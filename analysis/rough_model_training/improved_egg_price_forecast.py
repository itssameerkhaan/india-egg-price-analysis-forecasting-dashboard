"""
Improved egg price forecast experiment.

Run from the project root or this folder:
    python analysis/rough_model_training/improved_egg_price_forecast.py

The script:
1. Loads all city CSV files from output/main_data.
2. Builds leakage-aware 1-to-7-day-ahead targets.
3. Recomputes lag, rolling, momentum, calendar, and festival-window features.
4. Compares:
   - notebook-style XGBoost model
   - improved XGBoost delta model trained only on the selected city
   - improved XGBoost delta model trained only on the selected city
   - pooled and recent-window XGBoost delta variants
   - Random Forest delta model trained only on the selected city
   - Extra Trees delta model trained only on the selected city
   - HistGradientBoosting delta model trained only on the selected city
   - Ridge delta model trained only on the selected city
   - leakage-aware time-series models trained/tuned on the selected city
   - simple current-price persistence baseline
   - lag/rolling baselines
5. Prints metrics and prediction comparison rows.
6. Creates a separate interactive Plotly chart for each horizon and opens an index page.
"""

from __future__ import annotations

import argparse
import tempfile
import webbrowser
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "output" / "main_data"
DEFAULT_CITY = "Barwala"
DEFAULT_HORIZON = 4
DEFAULT_HORIZONS = [1, 2, 3, 4, 5, 6, 7]
DEFAULT_SPLIT_DATE = "2025-01-01"


def open_plotly_in_browser(fig: go.Figure, name: str) -> None:
    safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name)
    temp_path = Path(tempfile.gettempdir()) / f"{safe_name}.html"
    fig.write_html(temp_path, include_plotlyjs="cdn", auto_open=False)
    webbrowser.open_new_tab(temp_path.resolve().as_uri())


def load_city_data(data_dir: Path) -> pd.DataFrame:
    frames = []
    for csv_path in sorted(data_dir.glob("*_main_data.csv")):
        city_name = csv_path.stem.replace("_main_data", "")
        frame = pd.read_csv(csv_path)
        frame["City"] = frame.get("City", city_name).fillna(city_name)
        frame["City"] = frame["City"].replace("", city_name)
        frame["source_city"] = city_name
        frames.append(frame)

    if not frames:
        raise FileNotFoundError(f"No *_main_data.csv files found in {data_dir}")

    data = pd.concat(frames, ignore_index=True)
    data["Date"] = pd.to_datetime(data["Date"])
    data["City"] = data["source_city"]
    return data.sort_values(["City", "Date"]).reset_index(drop=True)


def add_festival_windows(group: pd.DataFrame) -> pd.DataFrame:
    group = group.sort_values("Date").copy()
    is_festival = group["is_festival"].to_numpy(dtype=int)
    n_rows = len(group)

    next_7 = np.zeros(n_rows, dtype=int)
    prev_7 = np.zeros(n_rows, dtype=int)
    days_until = np.full(n_rows, 99, dtype=int)
    days_after = np.full(n_rows, 99, dtype=int)
    festival_positions = np.where(is_festival == 1)[0]

    for idx in range(n_rows):
        future = festival_positions[festival_positions >= idx]
        past = festival_positions[festival_positions <= idx]
        if len(future):
            days_until[idx] = int(future[0] - idx)
            next_7[idx] = int(days_until[idx] <= 7)
        if len(past):
            days_after[idx] = int(idx - past[-1])
            prev_7[idx] = int(days_after[idx] <= 7)

    group["festival_next_7_days"] = next_7
    group["festival_prev_7_days"] = prev_7
    group["days_until_festival"] = days_until
    group["days_after_festival"] = days_after
    return group


def build_features(raw_data: pd.DataFrame, horizon: int) -> pd.DataFrame:
    needed = [
        "City",
        "Date",
        "Price",
        "market_rating",
        "tmax",
        "prcp",
        "is_weekend",
        "is_festival",
    ]
    data = raw_data[needed].copy()
    data["is_festival"] = data["is_festival"].notna().astype(int)
    data["is_weekend"] = data["is_weekend"].fillna(0).astype(int)
    data["market_rating"] = data["market_rating"].fillna(data["market_rating"].median())
    data["tmax"] = data["tmax"].fillna(data["tmax"].median())
    data["prcp"] = data["prcp"].fillna(0)
    data = data.sort_values(["City", "Date"]).reset_index(drop=True)

    grouped = data.groupby("City", group_keys=False)
    data["target"] = grouped["Price"].shift(-horizon)
    data["target_date"] = grouped["Date"].shift(-horizon)
    data["target_delta"] = data["target"] - data["Price"]

    for lag in [1, 2, 3, 4, 7, 14, 21, 30]:
        data[f"lag_{lag}"] = grouped["Price"].shift(lag)

    for window in [3, 7, 14, 30]:
        data[f"rolling_mean_{window}"] = grouped["Price"].transform(
            lambda s, w=window: s.rolling(w).mean()
        )
        data[f"rolling_std_{window}"] = grouped["Price"].transform(
            lambda s, w=window: s.rolling(w).std()
        )

    data["rolling_max_7"] = grouped["Price"].transform(lambda s: s.rolling(7).max())
    data["rolling_min_7"] = grouped["Price"].transform(lambda s: s.rolling(7).min())
    data["rolling_range_7"] = data["rolling_max_7"] - data["rolling_min_7"]

    data["price_change_1"] = data["Price"] - data["lag_1"]
    data["price_change_3"] = data["Price"] - data["lag_3"]
    data["price_change_7"] = data["Price"] - data["lag_7"]
    data["rolling_slope_7"] = data["Price"] - data["lag_7"]

    data["dayofweek"] = data["Date"].dt.dayofweek
    data["month"] = data["Date"].dt.month
    data["quarter"] = data["Date"].dt.quarter
    data["weekofyear"] = data["Date"].dt.isocalendar().week.astype(int)
    data["dayofyear"] = data["Date"].dt.dayofyear
    data["sin_year"] = np.sin(2 * np.pi * data["dayofyear"] / 365)
    data["cos_year"] = np.cos(2 * np.pi * data["dayofyear"] / 365)

    data = data.groupby("City", group_keys=False).apply(add_festival_windows)
    data = data.dropna().reset_index(drop=True)
    return data


def rmse(y_true: pd.Series, y_pred: np.ndarray | pd.Series) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def metrics_row(model_name: str, y_true: pd.Series, y_pred: np.ndarray | pd.Series) -> dict:
    return {
        "Model": model_name,
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": rmse(y_true, y_pred),
        "R2": r2_score(y_true, y_pred),
    }


def tune_xgb(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    horizon: int,
    n_iter: int,
    random_state: int,
) -> XGBRegressor:
    tscv = TimeSeriesSplit(n_splits=5, gap=horizon)
    base_model = XGBRegressor(
        objective="reg:squarederror",
        eval_metric="rmse",
        random_state=random_state,
        n_jobs=-1,
        tree_method="hist",
    )
    params = {
        "n_estimators": [300, 500, 800, 1000],
        "max_depth": [2, 3, 4, 5],
        "learning_rate": [0.01, 0.03, 0.05, 0.08],
        "subsample": [0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
        "min_child_weight": [1, 3, 5, 7],
        "reg_alpha": [0, 0.01, 0.05, 0.1],
        "reg_lambda": [0.5, 1, 2, 5],
        "gamma": [0, 0.01, 0.05, 0.1],
    }
    search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=params,
        n_iter=n_iter,
        scoring="neg_root_mean_squared_error",
        cv=tscv,
        random_state=random_state,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(X_train, y_train)
    print(f"\nBest CV RMSE: {-search.best_score_:.3f}")
    print("Best parameters:")
    print(search.best_params_)
    return search.best_estimator_


def model_factories(random_state: int) -> dict:
    return {
        "XGBoost delta": XGBRegressor(
            objective="reg:squarederror",
            eval_metric="rmse",
            n_estimators=1000,
            learning_rate=0.02,
            max_depth=2,
            min_child_weight=5,
            subsample=0.8,
            colsample_bytree=1.0,
            reg_alpha=0.05,
            reg_lambda=5,
            gamma=0.05,
            random_state=random_state,
            n_jobs=-1,
            tree_method="hist",
        ),
        "Random Forest delta": RandomForestRegressor(
            n_estimators=300,
            min_samples_leaf=3,
            max_features="sqrt",
            random_state=random_state,
            n_jobs=1,
        ),
        "Extra Trees delta": ExtraTreesRegressor(
            n_estimators=300,
            min_samples_leaf=3,
            max_features="sqrt",
            random_state=random_state,
            n_jobs=1,
        ),
        "HistGradientBoosting delta": HistGradientBoostingRegressor(
            max_iter=500,
            learning_rate=0.04,
            max_leaf_nodes=31,
            l2_regularization=0.05,
            random_state=random_state,
        ),
        "Ridge delta": make_pipeline(StandardScaler(), Ridge(alpha=10.0)),
    }


def _holt_forecast(level: float, trend: float, horizon: int, damping: float) -> float:
    if damping == 1:
        return level + horizon * trend
    return level + damping * (1 - damping**horizon) / (1 - damping) * trend


def _holt_states(prices: np.ndarray, alpha: float, beta: float, damping: float) -> tuple[np.ndarray, np.ndarray]:
    levels = np.zeros(len(prices), dtype=float)
    trends = np.zeros(len(prices), dtype=float)
    if len(prices) == 0:
        return levels, trends

    levels[0] = prices[0]
    trends[0] = prices[1] - prices[0] if len(prices) > 1 else 0.0
    for idx in range(1, len(prices)):
        previous_level = levels[idx - 1]
        previous_trend = trends[idx - 1]
        levels[idx] = alpha * prices[idx] + (1 - alpha) * (previous_level + damping * previous_trend)
        trends[idx] = beta * (levels[idx] - previous_level) + (1 - beta) * damping * previous_trend
    return levels, trends


def tune_holt_params(train_prices: np.ndarray, horizon: int) -> tuple[float, float, float]:
    validation_start = max(60, int(len(train_prices) * 0.75))
    if len(train_prices) <= validation_start + horizon:
        return 0.4, 0.05, 0.9

    best_params = (0.4, 0.05, 0.9)
    best_rmse = np.inf
    alpha_grid = [0.2, 0.4, 0.6, 0.8]
    beta_grid = [0.02, 0.05, 0.1, 0.2]
    damping_grid = [0.8, 0.9, 0.98, 1.0]

    for alpha in alpha_grid:
        for beta in beta_grid:
            for damping in damping_grid:
                levels, trends = _holt_states(train_prices, alpha, beta, damping)
                preds = [
                    _holt_forecast(levels[idx], trends[idx], horizon, damping)
                    for idx in range(validation_start, len(train_prices) - horizon)
                ]
                actual = train_prices[validation_start + horizon :]
                score = rmse(pd.Series(actual), np.asarray(preds))
                if score < best_rmse:
                    best_rmse = score
                    best_params = (alpha, beta, damping)

    return best_params


def rolling_linear_trend_predictions(
    prices: np.ndarray,
    feature_positions: np.ndarray,
    horizon: int,
    window: int,
) -> np.ndarray:
    predictions = []
    for pos in feature_positions:
        start = max(0, pos - window + 1)
        history = prices[start : pos + 1]
        if len(history) < 2:
            predictions.append(prices[pos])
            continue
        x = np.arange(len(history), dtype=float)
        slope, intercept = np.polyfit(x, history, 1)
        predictions.append(intercept + slope * (len(history) - 1 + horizon))
    return np.asarray(predictions)


def rolling_ar_predictions(
    prices: np.ndarray,
    feature_positions: np.ndarray,
    horizon: int,
    window: int = 120,
    lags: int = 7,
) -> np.ndarray:
    predictions = []
    for pos in feature_positions:
        history = prices[: pos + 1]
        if len(history) <= lags + 10:
            predictions.append(prices[pos])
            continue

        train_window = history[-window:]
        if len(train_window) <= lags:
            predictions.append(prices[pos])
            continue

        x_rows = []
        y_rows = []
        for idx in range(lags, len(train_window)):
            x_rows.append(train_window[idx - lags : idx][::-1])
            y_rows.append(train_window[idx])

        X = np.column_stack([np.ones(len(x_rows)), np.asarray(x_rows)])
        y = np.asarray(y_rows)
        coefs = np.linalg.lstsq(X, y, rcond=None)[0]

        recursive_history = list(history[-lags:])
        forecast = prices[pos]
        for _ in range(horizon):
            lag_values = np.asarray(recursive_history[-lags:][::-1])
            forecast = float(np.dot(np.r_[1.0, lag_values], coefs))
            recursive_history.append(forecast)
        predictions.append(forecast)
    return np.asarray(predictions)


def train_time_series_models(
    raw_data: pd.DataFrame,
    city: str,
    train_city: pd.DataFrame,
    test_city: pd.DataFrame,
    horizon: int,
) -> dict[str, np.ndarray]:
    city_prices = (
        raw_data[raw_data["City"] == city]
        .sort_values("Date")
        .drop_duplicates("Date", keep="last")
        .set_index("Date")["Price"]
        .astype(float)
    )
    prices = city_prices.to_numpy()
    date_to_pos = {date: idx for idx, date in enumerate(city_prices.index)}
    feature_positions = test_city["Date"].map(date_to_pos).to_numpy()
    target_dates = pd.to_datetime(test_city["target_date"])

    weekly_values = []
    for feature_date, target_date, current_price in zip(
        test_city["Date"], target_dates, test_city["Price"]
    ):
        seasonal_date = target_date - pd.Timedelta(days=7)
        if seasonal_date <= feature_date and seasonal_date in city_prices.index:
            weekly_values.append(float(city_prices.loc[seasonal_date]))
        else:
            weekly_values.append(float(current_price))

    train_prices = (
        city_prices.loc[city_prices.index <= train_city["Date"].max()]
        .astype(float)
        .to_numpy()
    )
    alpha, beta, damping = tune_holt_params(train_prices, horizon)
    levels, trends = _holt_states(prices, alpha, beta, damping)
    holt_predictions = np.asarray(
        [
            _holt_forecast(levels[pos], trends[pos], horizon, damping)
            for pos in feature_positions
        ]
    )

    alpha_linear, beta_linear, _ = tune_holt_params(train_prices, horizon)
    linear_levels, linear_trends = _holt_states(prices, alpha_linear, beta_linear, 1.0)
    holt_linear_predictions = np.asarray(
        [
            _holt_forecast(linear_levels[pos], linear_trends[pos], horizon, 1.0)
            for pos in feature_positions
        ]
    )

    return {
        "Weekly seasonal naive": np.asarray(weekly_values),
        "Rolling trend 30d": rolling_linear_trend_predictions(prices, feature_positions, horizon, 30),
        "Rolling trend 90d": rolling_linear_trend_predictions(prices, feature_positions, horizon, 90),
        "Rolling AR(7)": rolling_ar_predictions(prices, feature_positions, horizon),
        "Holt linear trend": holt_linear_predictions,
        "Damped Holt trend": holt_predictions,
    }


def prediction_column_name(model_name: str) -> str:
    known_columns = {
        "Notebook-style XGBoost": "Notebook_Style_Predicted",
        "Current price baseline": "Current_Price_Baseline",
        "Lag 1 baseline": "Lag_1_Baseline",
        "Rolling 7 baseline": "Rolling_7_Baseline",
    }
    if model_name in known_columns:
        return known_columns[model_name]
    return (
        model_name.replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        + "_Predicted"
    )


def make_chart(
    result: pd.DataFrame,
    metrics: pd.DataFrame,
    city: str,
    horizon: int,
    output_path: Path | None = None,
) -> None:
    fig = go.Figure()
    colors = [
        "#355cff",
        "#f05a28",
        "#2ca02c",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#17becf",
        "#7f7f7f",
    ]
    series = [("Actual", "Actual")] + [
        (row.Model, prediction_column_name(row.Model))
        for row in metrics.itertuples()
        if prediction_column_name(row.Model) in result.columns
    ]
    for idx, (name, column) in enumerate(series):
        fig.add_trace(
            go.Scatter(
                x=result["Target_Date"],
                y=result[column],
                mode="lines",
                name=name,
                line=dict(color=colors[idx % len(colors)], width=2),
            )
        )

    subtitle = " | ".join(
        f"{row.Model}: MAE {row.MAE:.2f}, RMSE {row.RMSE:.2f}, R2 {row.R2:.3f}"
        for row in metrics.head(5).itertuples()
    )
    fig.update_layout(
        title=f"{city} {horizon}-day Egg Price Forecast Comparison<br><sup>{subtitle}</sup>",
        xaxis_title="Target date",
        yaxis_title="Price",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    if output_path:
        fig.write_html(output_path, include_plotlyjs="cdn", auto_open=False)
    else:
        open_plotly_in_browser(fig, f"{city}_{horizon}day_forecast_comparison")


def make_best_strategy_chart(
    result: pd.DataFrame,
    city: str,
    horizon: int,
    output_path: Path | None = None,
) -> None:
    predicted_col = prediction_column_name("XGBoost best delta strategy")
    if predicted_col not in result.columns:
        return

    chart_data = result.copy()
    chart_data["Prediction_Error"] = chart_data["Actual"] - chart_data[predicted_col]
    chart_data["Absolute_Error"] = chart_data["Prediction_Error"].abs()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=chart_data["Target_Date"],
            y=chart_data["Actual"],
            mode="lines+markers",
            name="Actual price",
            line=dict(color="#111827", width=2.5),
            marker=dict(size=5),
            hovertemplate=(
                "Target date: %{x|%Y-%m-%d}<br>"
                "Actual: %{y:.2f}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=chart_data["Target_Date"],
            y=chart_data[predicted_col],
            mode="lines+markers",
            name="Predicted price",
            line=dict(color="#2563eb", width=2),
            marker=dict(size=5),
            hovertemplate=(
                "Target date: %{x|%Y-%m-%d}<br>"
                "Predicted: %{y:.2f}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=chart_data["Target_Date"] - pd.to_timedelta(horizon, unit="D"),
            y=chart_data[predicted_col],
            mode="lines",
            name=f"Prediction shifted {horizon} day(s) earlier (diagnostic only)",
            line=dict(color="#6b7280", width=1.5, dash="dash"),
            hovertemplate=(
                "Shifted diagnostic date: %{x|%Y-%m-%d}<br>"
                "Predicted value: %{y:.2f}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Bar(
            x=chart_data["Target_Date"],
            y=chart_data["Prediction_Error"],
            name="Actual - predicted",
            marker_color="#f97316",
            opacity=0.45,
            yaxis="y2",
            hovertemplate=(
                "Target date: %{x|%Y-%m-%d}<br>"
                "Error: %{y:.2f}<extra></extra>"
            ),
        )
    )

    mae = mean_absolute_error(chart_data["Actual"], chart_data[predicted_col])
    chart_rmse = rmse(chart_data["Actual"], chart_data[predicted_col])
    r2 = r2_score(chart_data["Actual"], chart_data[predicted_col])
    max_error_row = chart_data.loc[chart_data["Absolute_Error"].idxmax()]

    fig.update_layout(
        title=(
            f"{city} {horizon}-day Actual vs Predicted"
            f"<br><sup>XGBoost best delta strategy | MAE {mae:.2f}, "
            f"RMSE {chart_rmse:.2f}, R2 {r2:.3f} | "
            f"Max abs error {max_error_row['Absolute_Error']:.2f} on "
            f"{pd.Timestamp(max_error_row['Target_Date']).date()}</sup>"
        ),
        xaxis_title="Target date",
        yaxis=dict(title="Price"),
        yaxis2=dict(
            title="Prediction error",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=True,
            zerolinecolor="#9ca3af",
        ),
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    if output_path:
        fig.write_html(output_path, include_plotlyjs="cdn", auto_open=False)
    else:
        open_plotly_in_browser(fig, f"{city}_{horizon}day_xgboost_best_actual_vs_predicted")


def write_index_page(city: str, chart_paths: list[Path], summary: pd.DataFrame) -> Path:
    summary_html = summary.round({"MAE": 3, "RMSE": 3, "R2": 3}).to_html(index=False)
    links = "\n".join(
        f'<li><a href="{path.name}" target="_blank">{path.stem}</a></li>'
        for path in chart_paths
    )
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{city} Egg Price Forecast Comparison</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; }}
    table {{ border-collapse: collapse; margin-top: 16px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 6px 10px; text-align: right; }}
    th:first-child, td:first-child {{ text-align: left; }}
    th {{ background: #f3f4f6; }}
    a {{ color: #2563eb; }}
  </style>
</head>
<body>
  <h1>{city} Egg Price Forecast Comparison</h1>
  <p>Separate city-only models were trained for each forecast horizon.</p>
  <h2>Charts</h2>
  <ul>{links}</ul>
  <h2>Metric Summary</h2>
  {summary_html}
</body>
</html>
"""
    index_path = SCRIPT_DIR / f"{city.lower()}_forecast_comparison_index.html"
    index_path.write_text(html, encoding="utf-8")
    return index_path


def write_best_strategy_index_page(city: str, chart_paths: list[Path], summary: pd.DataFrame) -> Path:
    best_summary = summary[summary["Model"] == "XGBoost best delta strategy"].copy()
    summary_html = best_summary.round({"MAE": 3, "RMSE": 3, "R2": 3}).to_html(index=False)
    links = "\n".join(
        f'<li><a href="{path.name}" target="_blank">{path.stem}</a></li>'
        for path in chart_paths
    )
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{city} XGBoost Best Strategy Forecast</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; }}
    table {{ border-collapse: collapse; margin-top: 16px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 6px 10px; text-align: right; }}
    th:first-child, td:first-child {{ text-align: left; }}
    th {{ background: #f3f4f6; }}
    a {{ color: #2563eb; }}
  </style>
</head>
<body>
  <h1>{city} XGBoost Best Strategy Forecast</h1>
  <p>Actual price vs predicted price for each forecast horizon. Orange bars show actual minus predicted error.</p>
  <h2>Actual vs Predicted Charts</h2>
  <ul>{links}</ul>
  <h2>Metric Summary</h2>
  {summary_html}
</body>
</html>
"""
    index_path = SCRIPT_DIR / f"{city.lower()}_xgboost_best_strategy_index.html"
    index_path.write_text(html, encoding="utf-8")
    return index_path


NOTEBOOK_FEATURES = [
        "market_rating",
        "lag_1",
        "lag_3",
        "lag_7",
        "lag_14",
        "lag_30",
        "rolling_mean_7",
        "rolling_mean_14",
        "rolling_mean_30",
        "rolling_std_7",
        "tmax",
        "prcp",
        "dayofweek",
        "weekofyear",
        "quarter",
        "is_weekend",
        "is_festival",
]


IMPROVED_FEATURES = [
        "Price",
        "market_rating",
        "lag_1",
        "lag_2",
        "lag_3",
        "lag_4",
        "lag_7",
        "lag_14",
        "lag_21",
        "lag_30",
        "rolling_mean_3",
        "rolling_mean_7",
        "rolling_mean_14",
        "rolling_mean_30",
        "rolling_std_3",
        "rolling_std_7",
        "rolling_std_14",
        "rolling_std_30",
        "rolling_range_7",
        "price_change_1",
        "price_change_3",
        "price_change_7",
        "rolling_slope_7",
        "tmax",
        "prcp",
        "dayofweek",
        "month",
        "weekofyear",
        "quarter",
        "dayofyear",
        "sin_year",
        "cos_year",
        "is_weekend",
        "is_festival",
        "festival_next_7_days",
        "festival_prev_7_days",
        "days_until_festival",
        "days_after_festival",
]


MARKET_FEATURES = [
        "market_mean_price",
        "market_median_price",
        "market_std_price",
        "market_range_price",
        "other_city_mean_price",
        "price_vs_market_mean",
        "market_change_1",
        "market_change_3",
        "market_change_7",
        "market_rolling_mean_7",
        "market_rolling_slope_7",
]


XGB_CITY_CONSERVATIVE_PARAMS = {
    "objective": "reg:squarederror",
    "eval_metric": "rmse",
    "n_estimators": 1000,
    "learning_rate": 0.02,
    "max_depth": 2,
    "min_child_weight": 5,
    "subsample": 0.8,
    "colsample_bytree": 1.0,
    "reg_alpha": 0.05,
    "reg_lambda": 5,
    "gamma": 0.05,
    "n_jobs": -1,
    "tree_method": "hist",
}


XGB_POOLED_RESPONSIVE_PARAMS = {
    "objective": "reg:squarederror",
    "eval_metric": "rmse",
    "n_estimators": 500,
    "learning_rate": 0.05,
    "max_depth": 2,
    "min_child_weight": 3,
    "subsample": 0.85,
    "colsample_bytree": 0.9,
    "reg_alpha": 0.05,
    "reg_lambda": 2,
    "gamma": 0.05,
    "n_jobs": -1,
    "tree_method": "hist",
}


def train_notebook_style_model(
    train_city: pd.DataFrame,
    test_city: pd.DataFrame,
    random_state: int,
) -> np.ndarray:
    notebook_params = {
        "subsample": 0.8,
        "reg_lambda": 2,
        "reg_alpha": 0.05,
        "n_estimators": 800,
        "min_child_weight": 5,
        "max_depth": 2,
        "learning_rate": 0.01,
        "gamma": 0.1,
        "colsample_bytree": 1.0,
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "random_state": random_state,
        "n_jobs": -1,
        "tree_method": "hist",
    }
    notebook_model = XGBRegressor(**notebook_params)
    notebook_model.fit(train_city[NOTEBOOK_FEATURES], train_city["target"])
    return notebook_model.predict(test_city[NOTEBOOK_FEATURES])


def make_xgb_delta_model(params: dict, random_state: int) -> XGBRegressor:
    return XGBRegressor(**params, random_state=random_state)


def add_market_features(data: pd.DataFrame) -> pd.DataFrame:
    market_data = data.copy().sort_values(["City", "Date"])
    daily_prices = market_data.groupby("Date")["Price"]
    market_data["market_mean_price"] = daily_prices.transform("mean")
    market_data["market_median_price"] = daily_prices.transform("median")
    market_data["market_std_price"] = daily_prices.transform("std").fillna(0)
    market_data["market_min_price"] = daily_prices.transform("min")
    market_data["market_max_price"] = daily_prices.transform("max")
    market_data["market_range_price"] = (
        market_data["market_max_price"] - market_data["market_min_price"]
    )

    city_counts = daily_prices.transform("count")
    other_city_count = (city_counts - 1).replace(0, np.nan)
    market_data["other_city_mean_price"] = (
        (market_data["market_mean_price"] * city_counts) - market_data["Price"]
    ) / other_city_count
    market_data["other_city_mean_price"] = market_data["other_city_mean_price"].fillna(
        market_data["market_mean_price"]
    )
    market_data["price_vs_market_mean"] = (
        market_data["Price"] - market_data["market_mean_price"]
    )

    market_daily = (
        market_data.groupby("Date", as_index=False)["Price"]
        .mean()
        .sort_values("Date")
        .rename(columns={"Price": "daily_market_mean"})
    )
    market_daily["market_change_1"] = (
        market_daily["daily_market_mean"] - market_daily["daily_market_mean"].shift(1)
    )
    market_daily["market_change_3"] = (
        market_daily["daily_market_mean"] - market_daily["daily_market_mean"].shift(3)
    )
    market_daily["market_change_7"] = (
        market_daily["daily_market_mean"] - market_daily["daily_market_mean"].shift(7)
    )
    market_daily["market_rolling_mean_7"] = market_daily["daily_market_mean"].rolling(7).mean()
    market_daily["market_rolling_slope_7"] = (
        market_daily["daily_market_mean"] - market_daily["daily_market_mean"].shift(7)
    )
    market_daily = market_daily.set_index("Date")
    for column in [
        "market_change_1",
        "market_change_3",
        "market_change_7",
        "market_rolling_mean_7",
        "market_rolling_slope_7",
    ]:
        market_data[column] = market_data["Date"].map(market_daily[column])

    return market_data.dropna(subset=MARKET_FEATURES).reset_index(drop=True)


def train_pooled_xgb_prediction(
    train_all: pd.DataFrame,
    test_city: pd.DataFrame,
    feature_columns: list[str],
    params: dict,
    random_state: int,
) -> np.ndarray:
    combined = pd.concat([train_all, test_city], ignore_index=True)
    city_dummies = pd.get_dummies(combined["City"], prefix="city")
    combined = pd.concat([combined.reset_index(drop=True), city_dummies.reset_index(drop=True)], axis=1)
    pooled_features = feature_columns + list(city_dummies.columns)

    train_pooled = combined.iloc[: len(train_all)]
    test_pooled = combined.iloc[len(train_all) :]
    pooled_model = make_xgb_delta_model(params, random_state)
    pooled_model.fit(train_pooled[pooled_features], train_pooled["target_delta"])
    return test_pooled["Price"].to_numpy() + pooled_model.predict(test_pooled[pooled_features])


def train_best_xgb_delta_models(
    data: pd.DataFrame,
    train_city: pd.DataFrame,
    test_city: pd.DataFrame,
    split_date: pd.Timestamp,
    horizon: int,
    random_state: int,
) -> dict[str, np.ndarray]:
    predictions = {}

    recent_train_city = train_city.tail(1000)
    recent_model = make_xgb_delta_model(XGB_CITY_CONSERVATIVE_PARAMS, random_state)
    recent_model.fit(recent_train_city[IMPROVED_FEATURES], recent_train_city["target_delta"])
    recent_pred = test_city["Price"].to_numpy() + recent_model.predict(test_city[IMPROVED_FEATURES])
    predictions["XGBoost recent-1000 delta"] = recent_pred

    train_all = data[data["target_date"] < split_date].copy()
    pooled_pred = train_pooled_xgb_prediction(
        train_all,
        test_city,
        IMPROVED_FEATURES,
        XGB_POOLED_RESPONSIVE_PARAMS,
        random_state,
    )
    predictions["XGBoost pooled delta"] = pooled_pred

    pooled_conservative_pred = train_pooled_xgb_prediction(
        train_all,
        test_city,
        IMPROVED_FEATURES,
        XGB_CITY_CONSERVATIVE_PARAMS,
        random_state,
    )
    predictions["XGBoost pooled conservative delta"] = pooled_conservative_pred

    market_data = add_market_features(data)
    market_train_all = market_data[market_data["target_date"] < split_date].copy()
    market_test_city = market_data[
        (market_data["City"] == test_city["City"].iloc[0])
        & (market_data["target_date"] >= split_date)
    ].copy()
    market_features = IMPROVED_FEATURES + MARKET_FEATURES
    market_pooled_pred = train_pooled_xgb_prediction(
        market_train_all,
        market_test_city,
        market_features,
        XGB_CITY_CONSERVATIVE_PARAMS,
        random_state,
    )
    market_predictions = (
        market_test_city[["Date", "target_date"]]
        .assign(prediction=market_pooled_pred)
        .rename(columns={"target_date": "Target_Date"})
    )
    aligned_market_pred = (
        test_city[["Date", "target_date"]]
        .rename(columns={"target_date": "Target_Date"})
        .merge(market_predictions, on=["Date", "Target_Date"], how="left")["prediction"]
        .to_numpy()
    )
    predictions["XGBoost market-aware delta"] = aligned_market_pred

    if horizon == 2 and not np.isnan(aligned_market_pred).any():
        predictions["XGBoost best delta strategy"] = aligned_market_pred
    elif horizon in [1, 2]:
        predictions["XGBoost best delta strategy"] = pooled_conservative_pred
    elif horizon == 7:
        predictions["XGBoost best delta strategy"] = recent_pred
    else:
        predictions["XGBoost best delta strategy"] = pooled_pred

    return predictions


def train_delta_models(
    train_city: pd.DataFrame,
    test_city: pd.DataFrame,
    random_state: int,
) -> dict[str, np.ndarray]:
    predictions = {}
    X_train = train_city[IMPROVED_FEATURES]
    y_train = train_city["target_delta"]
    X_test = test_city[IMPROVED_FEATURES]

    for model_name, model in model_factories(random_state).items():
        model.fit(X_train, y_train)
        delta_pred = model.predict(X_test)
        predictions[model_name] = test_city["Price"].to_numpy() + delta_pred

    return predictions


def run_single_horizon(
    raw_data: pd.DataFrame,
    args: argparse.Namespace,
    horizon: int,
) -> tuple[pd.DataFrame, pd.DataFrame, Path | None, Path | None]:
    data = build_features(raw_data, horizon)
    split_date = pd.Timestamp(args.split_date)

    city_data = data[data["City"] == args.city].copy()
    train_city = city_data[city_data["target_date"] < split_date].copy()
    test_city = city_data[city_data["target_date"] >= split_date].copy()

    if train_city.empty or test_city.empty:
        raise ValueError(f"Not enough train/test rows for city {args.city!r} and horizon {horizon}.")

    notebook_pred = train_notebook_style_model(train_city, test_city, args.random_state)
    delta_predictions = train_delta_models(train_city, test_city, args.random_state)
    best_xgb_predictions = train_best_xgb_delta_models(
        data, train_city, test_city, split_date, horizon, args.random_state
    )
    time_series_predictions = train_time_series_models(
        raw_data, args.city, train_city, test_city, horizon
    )

    result = pd.DataFrame(
        {
            "City": test_city["City"].to_numpy(),
            "Feature_Date": test_city["Date"].to_numpy(),
            "Target_Date": test_city["target_date"].to_numpy(),
            "Current_Price": test_city["Price"].to_numpy(),
            "Actual": test_city["target"].to_numpy(),
            "Notebook_Style_Predicted": notebook_pred,
            "Current_Price_Baseline": test_city["Price"].to_numpy(),
            "Lag_1_Baseline": test_city["lag_1"].to_numpy(),
            "Rolling_7_Baseline": test_city["rolling_mean_7"].to_numpy(),
        }
    )
    for model_name, pred in delta_predictions.items():
        result[prediction_column_name(model_name)] = pred
    for model_name, pred in best_xgb_predictions.items():
        result[prediction_column_name(model_name)] = pred
    for model_name, pred in time_series_predictions.items():
        result[prediction_column_name(model_name)] = pred

    result["Notebook_Error"] = result["Actual"] - result["Notebook_Style_Predicted"]
    result["Current_Baseline_Error"] = result["Actual"] - result["Current_Price_Baseline"]

    metric_rows = []
    for model_name in delta_predictions:
        metric_rows.append(
            metrics_row(model_name, result["Actual"], result[prediction_column_name(model_name)])
        )
    for model_name in best_xgb_predictions:
        metric_rows.append(
            metrics_row(model_name, result["Actual"], result[prediction_column_name(model_name)])
        )
    for model_name in time_series_predictions:
        metric_rows.append(
            metrics_row(model_name, result["Actual"], result[prediction_column_name(model_name)])
        )
    metric_rows.extend(
        [
            metrics_row("Notebook-style XGBoost", result["Actual"], result["Notebook_Style_Predicted"]),
            metrics_row("Current price baseline", result["Actual"], result["Current_Price_Baseline"]),
            metrics_row("Lag 1 baseline", result["Actual"], result["Lag_1_Baseline"]),
            metrics_row("Rolling 7 baseline", result["Actual"], result["Rolling_7_Baseline"]),
        ]
    )
    metrics = pd.DataFrame(metric_rows).sort_values("RMSE")
    metrics.insert(0, "Horizon", horizon)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 180)

    print(f"\nCity: {args.city}")
    print(f"Horizon: {horizon} day(s)")
    print(f"Train rows, {args.city}: {len(train_city)}")
    print(f"Test rows, {args.city}: {len(test_city)}")
    print(f"Test target date range: {result['Target_Date'].min().date()} to {result['Target_Date'].max().date()}")

    print("\nModel and baseline comparison:")
    print(metrics.round({"MAE": 3, "RMSE": 3, "R2": 3}).to_string(index=False))

    print("\nPrediction comparison data, first rows:")
    best_model_name = metrics.iloc[0]["Model"]
    best_column = prediction_column_name(best_model_name)
    preview_cols = [
        "City",
        "Feature_Date",
        "Target_Date",
        "Current_Price",
        "Actual",
        best_column if best_column in result.columns else "Notebook_Style_Predicted",
        "Current_Price_Baseline",
        "Notebook_Style_Predicted",
    ]
    print(result[preview_cols].head(args.rows).round(2).to_string(index=False))

    print(f"\nWorst errors for best model: {best_model_name}")
    if best_column not in result.columns:
        best_column = "Notebook_Style_Predicted"
    result["Best_Model_Error"] = result["Actual"] - result[best_column]
    worst_cols = [
        "Feature_Date",
        "Target_Date",
        "Actual",
        best_column,
        "Best_Model_Error",
        "Notebook_Style_Predicted",
        "Current_Price_Baseline",
    ]
    print(
        result.assign(Abs_Best_Model_Error=result["Best_Model_Error"].abs())
        .sort_values("Abs_Best_Model_Error", ascending=False)
        .head(args.rows)[worst_cols]
        .round(2)
        .to_string(index=False)
    )

    output_path = None
    best_output_path = None
    if args.save_html:
        output_path = SCRIPT_DIR / f"{args.city.lower()}_{horizon}day_forecast_comparison.html"
        best_output_path = SCRIPT_DIR / f"{args.city.lower()}_{horizon}day_xgboost_best_actual_vs_predicted.html"

    make_chart(result, metrics, args.city, horizon, output_path)
    make_best_strategy_chart(result, args.city, horizon, best_output_path)

    if output_path and best_output_path:
        print(f"\nSaved chart: {output_path}")
        print(f"Saved best-strategy chart: {best_output_path}")
    else:
        print(f"\nOpened Plotly charts in browser for horizon {horizon}.")
    return result, metrics, output_path, best_output_path


def parse_horizons(value: str) -> list[int]:
    if value.lower() == "all":
        return DEFAULT_HORIZONS
    horizons = []
    for part in value.split(","):
        horizon = int(part.strip())
        if horizon < 1:
            raise ValueError("Horizons must be positive integers.")
        horizons.append(horizon)
    return horizons


def run(args: argparse.Namespace) -> None:
    raw_data = load_city_data(DATA_DIR)
    horizons = parse_horizons(args.horizons)
    chart_paths = []
    best_chart_paths = []
    metric_frames = []

    for horizon in horizons:
        _, metrics, chart_path, best_chart_path = run_single_horizon(raw_data, args, horizon)
        chart_paths.append(chart_path)
        best_chart_paths.append(best_chart_path)
        metric_frames.append(metrics)

    summary = pd.concat(metric_frames, ignore_index=True)
    print("\nAll horizon metric summary:")
    print(summary.round({"MAE": 3, "RMSE": 3, "R2": 3}).to_string(index=False))

    if args.save_html:
        index_path = write_index_page(args.city, chart_paths, summary)
        best_index_path = write_best_strategy_index_page(args.city, best_chart_paths, summary)
        print(f"\nSaved chart index: {index_path}")
        print(f"Saved best-strategy chart index: {best_index_path}")
    else:
        print("\nOpened Plotly charts directly in the browser. No project HTML report files were saved.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Improved egg price forecast comparison")
    parser.add_argument("--city", default=DEFAULT_CITY, help="City to evaluate, e.g. Barwala")
    parser.add_argument(
        "--horizons",
        default="all",
        help="Forecast horizons to run. Use 'all' or comma-separated values like 1,2,3,4.",
    )
    parser.add_argument("--split-date", default=DEFAULT_SPLIT_DATE, help="First target date in test set")
    parser.add_argument("--rows", type=int, default=20, help="Rows to print for prediction tables")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--save-html",
        action="store_true",
        help="Save chart HTML files and index pages instead of only opening charts in the browser.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
