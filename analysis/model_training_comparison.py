import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit

try:
    from xgboost import XGBRegressor
except ImportError as exc:
    raise ImportError("XGBoost is required. Install it with: pip install xgboost") from exc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_DATA_DIR = PROJECT_ROOT / "output" / "main_data"
COMPARE_DIR = PROJECT_ROOT / "output" / "forecast" / "compare"
FORECAST_DIR = PROJECT_ROOT / "output" / "forecast"
CHART_DIR = PROJECT_ROOT / "analysis" / "analysis_chart"

DEFAULT_CITY = "Barwala"
FEATURES_TRAIN = [
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
TARGET = "Price"


def log(message):
    print(f"[model-training] {message}", flush=True)


def daily_market_rating(change):
    if pd.isna(change):
        return 0
    if change >= 10:
        return 5
    if change >= 7:
        return 4
    if change >= 5:
        return 3
    if change >= 3:
        return 2
    if change >= 1:
        return 1
    if change <= -10:
        return -5
    if change <= -7:
        return -4
    if change <= -5:
        return -3
    if change <= -3:
        return -2
    if change <= -1:
        return -1
    return 0


def load_all_city_data():
    files = sorted(MAIN_DATA_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No city data CSV files found in {MAIN_DATA_DIR}")

    all_data = {}
    for file_path in files:
        all_data[file_path.stem] = pd.read_csv(file_path)

    log(f"Loaded {len(all_data)} city data files: {', '.join(all_data.keys())}")
    return all_data


def prepare_city_data(all_data, city):
    key = f"{city}_main_data"
    if key not in all_data:
        raise KeyError(f"{key} not found. Available data: {', '.join(all_data.keys())}")

    df = all_data[key].copy()
    log(f"Using {key}: raw shape {df.shape}")

    if "is_festival" in df.columns:
        df["is_festival"] = df["is_festival"].notna().astype(int)
    else:
        df["is_festival"] = 0

    drop_columns = [column for column in ["festival_name", "City", "Category"] if column in df.columns]
    df = df.drop(drop_columns, axis=1)
    df["Date"] = pd.to_datetime(df["Date"])

    for column in [TARGET] + FEATURES_TRAIN:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    missing_before = df[[TARGET] + FEATURES_TRAIN].isna().sum().sort_values(ascending=False)
    log("Missing values before dropna:")
    print(missing_before[missing_before > 0].to_string(), flush=True)

    df = df.dropna(subset=[TARGET] + FEATURES_TRAIN).sort_values("Date").reset_index(drop=True)
    log(f"Prepared model data shape after dropna: {df.shape}")
    log(f"Prepared date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    return df


def split_train_test(df, test_start_date, test_end_date):
    train_data = df[df["Date"] < test_start_date].copy()
    test_data = df[(df["Date"] >= test_start_date) & (df["Date"] <= test_end_date)].copy()

    if train_data.empty or test_data.empty:
        raise ValueError("Train/test split produced empty data. Check input dates.")

    x_train = train_data[FEATURES_TRAIN]
    y_train = train_data[TARGET]
    x_test = test_data[FEATURES_TRAIN]
    y_test = test_data[TARGET]

    log(f"Train rows: {len(train_data)} through {train_data['Date'].max().date()}")
    log(f"Test rows: {len(test_data)} from {test_data['Date'].min().date()} to {test_data['Date'].max().date()}")
    return train_data, test_data, x_train, y_train, x_test, y_test


def backtest_window(df):
    test_end_date = df["Date"].max()
    test_start_date = test_end_date - pd.DateOffset(years=1)
    forecast_days = (test_end_date - test_start_date).days + 1
    log(
        "Backtest window selected: "
        f"train before {test_start_date.date()}, recursive test from "
        f"{test_start_date.date()} to {test_end_date.date()} ({forecast_days} days)"
    )
    return test_start_date, test_end_date, forecast_days


def train_best_model(x_train, y_train):
    log("Training XGBoost with TimeSeriesSplit and RandomizedSearchCV")
    tscv = TimeSeriesSplit(n_splits=5)

    xgb_base = XGBRegressor(
        objective="reg:squarederror",
        eval_metric="rmse",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
    )

    param_distributions = {
        "n_estimators": [300, 500, 800, 1000],
        "max_depth": [2, 3, 4, 5, 6],
        "learning_rate": [0.01, 0.03, 0.05, 0.08, 0.1],
        "subsample": [0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
        "min_child_weight": [1, 3, 5, 7],
        "reg_alpha": [0, 0.01, 0.05, 0.1],
        "reg_lambda": [0.5, 1, 2, 5],
        "gamma": [0, 0.01, 0.05, 0.1],
    }

    search = RandomizedSearchCV(
        estimator=xgb_base,
        param_distributions=param_distributions,
        n_iter=60,
        scoring="neg_root_mean_squared_error",
        cv=tscv,
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(x_train, y_train)

    log(f"Best CV RMSE: {-search.best_score_:.3f}")
    log(f"Best parameters: {search.best_params_}")
    return search.best_estimator_, search


def recursive_forecast(model, df, start_date, forecast_days=30):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    current_date = pd.to_datetime(start_date)
    historical_prices = df[df["Date"] < current_date].set_index("Date")["Price"].to_dict()
    predictions = []

    if len(historical_prices) < 30:
        raise ValueError("Need at least 30 historical price rows before recursive forecast start.")

    log(f"Starting recursive forecast from {current_date.date()} for {forecast_days} days")
    for step in range(forecast_days):
        last_7 = [
            historical_prices.get(current_date - pd.Timedelta(days=i))
            for i in range(1, 8)
            if historical_prices.get(current_date - pd.Timedelta(days=i)) is not None
        ]
        last_14 = [
            historical_prices.get(current_date - pd.Timedelta(days=i))
            for i in range(1, 15)
            if historical_prices.get(current_date - pd.Timedelta(days=i)) is not None
        ]
        last_30 = [
            historical_prices.get(current_date - pd.Timedelta(days=i))
            for i in range(1, 31)
            if historical_prices.get(current_date - pd.Timedelta(days=i)) is not None
        ]

        external_row = df[df["Date"] == current_date]
        if len(external_row) > 0:
            tmax = external_row["tmax"].iloc[0]
            prcp = external_row["prcp"].iloc[0]
            is_festival = external_row["is_festival"].iloc[0]
        else:
            tmax = df["tmax"].mean()
            prcp = 0
            is_festival = 0

        previous_price = historical_prices.get(current_date - pd.Timedelta(days=1))
        previous_previous_price = historical_prices.get(current_date - pd.Timedelta(days=2))
        if previous_price is not None and previous_previous_price not in (None, 0):
            previous_change = ((previous_price - previous_previous_price) / previous_previous_price) * 100
        else:
            previous_change = np.nan
        market_rating = daily_market_rating(previous_change)

        feature_row = pd.DataFrame(
            [
                {
                    "market_rating": market_rating,
                    "lag_1": historical_prices.get(current_date - pd.Timedelta(days=1)),
                    "lag_3": historical_prices.get(current_date - pd.Timedelta(days=3)),
                    "lag_7": historical_prices.get(current_date - pd.Timedelta(days=7)),
                    "lag_14": historical_prices.get(current_date - pd.Timedelta(days=14)),
                    "lag_30": historical_prices.get(current_date - pd.Timedelta(days=30)),
                    "rolling_mean_7": np.mean(last_7),
                    "rolling_mean_14": np.mean(last_14),
                    "rolling_mean_30": np.mean(last_30),
                    "rolling_std_7": np.std(last_7),
                    "tmax": tmax,
                    "prcp": prcp,
                    "dayofweek": current_date.dayofweek,
                    "weekofyear": int(current_date.isocalendar().week),
                    "quarter": current_date.quarter,
                    "is_weekend": int(current_date.dayofweek >= 5),
                    "is_festival": is_festival,
                }
            ]
        )[FEATURES_TRAIN]

        prediction = round(float(model.predict(feature_row)[0]), 2)
        predictions.append({"Date": current_date, "Predicted_Price": prediction})
        historical_prices[current_date] = prediction
        log(f"Recursive day {step + 1:02d}: {current_date.date()} -> {prediction}")
        current_date += pd.Timedelta(days=1)

    return pd.DataFrame(predictions)


def make_test_results(test_data, recursive_predictions):
    test_results = test_data[["Date", TARGET]].copy()
    test_results["Date"] = pd.to_datetime(test_results["Date"])
    recursive_predictions = recursive_predictions.copy()
    recursive_predictions["Date"] = pd.to_datetime(recursive_predictions["Date"])
    test_results = test_results.merge(recursive_predictions, on="Date", how="inner")
    if test_results.empty:
        raise ValueError("No matching dates between actual test data and recursive predictions.")
    test_results["Error"] = test_results[TARGET] - test_results["Predicted_Price"]
    test_results["Absolute_Error"] = test_results["Error"].abs()
    test_results["Absolute_Percentage_Error"] = (test_results["Absolute_Error"] / test_results[TARGET]) * 100
    return test_results


def build_metrics(test_results, y_test):
    mae = mean_absolute_error(y_test, test_results["Predicted_Price"])
    rmse = root_mean_squared_error(y_test, test_results["Predicted_Price"])
    r2 = r2_score(y_test, test_results["Predicted_Price"])
    mape = np.mean(np.abs(test_results["Error"] / y_test)) * 100

    metrics = pd.DataFrame(
        {
            "Metric": ["MAE", "RMSE", "R2", "MAPE (%)"],
            "Value": [mae, rmse, r2, mape],
        }
    )
    metrics["Value"] = metrics["Value"].round(3)
    log(f"MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.3f}, MAPE={mape:.2f}%")
    return metrics


def actual_vs_predicted_figure(data, title, x_column="Date"):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data[x_column],
            y=data[TARGET],
            mode="lines+markers" if len(data) <= 60 else "lines",
            name="Actual price",
            line=dict(color="#1f77b4", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data[x_column],
            y=data["Predicted_Price"],
            mode="lines+markers" if len(data) <= 60 else "lines",
            name="Predicted price",
            line=dict(color="#d62728", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([data[x_column], data[x_column][::-1]]),
            y=pd.concat([data[TARGET], data["Predicted_Price"][::-1]]),
            fill="toself",
            fillcolor="rgba(244, 162, 97, 0.18)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name="Prediction gap",
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title=x_column.replace("_", " "),
        yaxis_title="Price",
        template="plotly_white",
        height=600,
        width=1300,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(tickangle=30)
    return fig


def save_backtest_outputs(test_results, city):
    COMPARE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    test_results = test_results.copy()
    test_results["Date"] = pd.to_datetime(test_results["Date"])

    test_results.to_csv(COMPARE_DIR / "test_recursive_actual_vs_predicted.csv", index=False)
    test_results.to_csv(COMPARE_DIR / "daily_1_year_compare.csv", index=False)
    actual_vs_predicted_figure(
        test_results,
        f"{city} recursive validation: daily actual vs predicted",
    ).write_html(CHART_DIR / "daily_1_year_compare.html")

    monthly_data = (
        test_results.assign(Month=test_results["Date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)
        .agg({TARGET: "mean", "Predicted_Price": "mean", "Error": "mean", "Absolute_Error": "mean"})
    )
    monthly_data[[TARGET, "Predicted_Price", "Error", "Absolute_Error"]] = monthly_data[
        [TARGET, "Predicted_Price", "Error", "Absolute_Error"]
    ].round(2)
    monthly_data.to_csv(COMPARE_DIR / "monthly_compare.csv", index=False)
    actual_vs_predicted_figure(
        monthly_data.rename(columns={"Month": "Period"}),
        f"{city} recursive validation: monthly actual vs predicted",
        x_column="Period",
    ).write_html(CHART_DIR / "monthly_compare.html")

    weekly_data = test_results.copy()
    weekly_data["Week_Start"] = weekly_data["Date"].dt.to_period("W-MON").apply(lambda period: period.start_time)
    weekly_data = (
        weekly_data.groupby("Week_Start", as_index=False)
        .agg({TARGET: "mean", "Predicted_Price": "mean", "Error": "mean", "Absolute_Error": "mean"})
    )
    weekly_data[[TARGET, "Predicted_Price", "Error", "Absolute_Error"]] = weekly_data[
        [TARGET, "Predicted_Price", "Error", "Absolute_Error"]
    ].round(2)
    weekly_data.to_csv(COMPARE_DIR / "weekly_compare.csv", index=False)
    actual_vs_predicted_figure(
        weekly_data,
        f"{city} recursive validation: weekly actual vs predicted",
        x_column="Week_Start",
    ).write_html(CHART_DIR / "weekly_compare.html")

    weekly_trend = weekly_data.copy()
    weekly_trend["Actual_Trend_4W"] = weekly_trend[TARGET].rolling(4, min_periods=1).mean().round(2)
    weekly_trend["Predicted_Trend_4W"] = weekly_trend["Predicted_Price"].rolling(4, min_periods=1).mean().round(2)
    weekly_trend["Trend_Gap"] = (weekly_trend["Actual_Trend_4W"] - weekly_trend["Predicted_Trend_4W"]).round(2)
    weekly_trend.to_csv(COMPARE_DIR / "weekly_trend_compare.csv", index=False)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=weekly_trend["Week_Start"],
            y=weekly_trend["Actual_Trend_4W"],
            mode="lines+markers",
            name="Actual weekly trend",
            line=dict(color="#2a9d8f", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=weekly_trend["Week_Start"],
            y=weekly_trend["Predicted_Trend_4W"],
            mode="lines+markers",
            name="Predicted weekly trend",
            line=dict(color="#e76f51", width=3),
        )
    )
    fig.update_layout(
        title=f"{city} recursive validation: weekly trend comparison (4-week rolling average)",
        xaxis_title="Week start",
        yaxis_title="Price",
        template="plotly_white",
        height=600,
        width=1300,
        hovermode="x unified",
    )
    fig.write_html(CHART_DIR / "weekly_trend_compare.html")

    log(f"Saved recursive validation CSV outputs to {COMPARE_DIR}")
    log(f"Saved chart HTML outputs to {CHART_DIR}")


def save_model_outputs(model, search, metrics, test_results, recursive_predictions, summary):
    COMPARE_DIR.mkdir(parents=True, exist_ok=True)
    FORECAST_DIR.mkdir(parents=True, exist_ok=True)

    metrics.to_csv(COMPARE_DIR / "model_metrics.csv", index=False)
    test_results.to_csv(COMPARE_DIR / "test_actual_vs_predicted.csv", index=False)

    feature_importance = pd.DataFrame(
        {"Feature": FEATURES_TRAIN, "Importance": model.feature_importances_}
    ).sort_values("Importance", ascending=False)
    feature_importance.to_csv(COMPARE_DIR / "feature_importance.csv", index=False)

    cv_results = pd.DataFrame(search.cv_results_).sort_values("rank_test_score")
    cv_results.to_csv(COMPARE_DIR / "randomized_search_cv_results.csv", index=False)

    recursive_predictions.to_csv(FORECAST_DIR / "recursive_predictions.csv", index=False)
    recursive_predictions.to_csv(COMPARE_DIR / "recursive_predictions.csv", index=False)
    with (COMPARE_DIR / "model_run_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    log("Saved metrics, feature importance, CV results, test predictions, and recursive forecast")


def parse_args():
    parser = argparse.ArgumentParser(description="Train and validate egg price prediction model.")
    parser.add_argument("--city", default=DEFAULT_CITY, help="City name matching output/main_data/<City>_main_data.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    log("Starting notebook-equivalent model training pipeline")
    all_data = load_all_city_data()
    df = prepare_city_data(all_data, args.city)
    test_start_date, test_end_date, forecast_days = backtest_window(df)
    train_data, test_data, x_train, y_train, x_test, y_test = split_train_test(df, test_start_date, test_end_date)
    model, search = train_best_model(x_train, y_train)

    first_recursive_row = test_data[test_data["Date"] == test_data["Date"].min()][FEATURES_TRAIN]
    log(f"First recursive-style test row prediction: {model.predict(first_recursive_row)[0]:.2f}")

    recursive_predictions = recursive_forecast(
        model=model,
        df=df,
        start_date=test_start_date,
        forecast_days=forecast_days,
    )
    test_results = make_test_results(test_data, recursive_predictions)
    metrics = build_metrics(test_results, test_results[TARGET])

    forecast_end_date = recursive_predictions["Date"].max().strftime("%Y-%m-%d")
    summary = {
        "city": args.city,
        "data_start_date": df["Date"].min().strftime("%Y-%m-%d"),
        "data_end_date": df["Date"].max().strftime("%Y-%m-%d"),
        "max_data_year": int(df["Year"].max()),
        "split_year": int(test_start_date.year - 1),
        "train_start_date": train_data["Date"].min().strftime("%Y-%m-%d"),
        "train_end_date": train_data["Date"].max().strftime("%Y-%m-%d"),
        "test_start_date": test_data["Date"].min().strftime("%Y-%m-%d"),
        "test_end_date": test_data["Date"].max().strftime("%Y-%m-%d"),
        "forecast_start_date": test_start_date.strftime("%Y-%m-%d"),
        "forecast_end_date": forecast_end_date,
        "forecast_days": int(forecast_days),
    }
    save_model_outputs(model, search, metrics, test_results, recursive_predictions, summary)
    save_backtest_outputs(test_results, args.city)
    log("Pipeline completed")


if __name__ == "__main__":
    main()
