"""
Trend-focused egg price forecast experiment.

Run from the project root:
    python analysis/rough_model_training/egg_price_trend_forecast.py

This script uses the best XGBoost delta strategy from improved_egg_price_forecast.py,
then evaluates price movement instead of only exact future price:
    - actual movement = actual future price - current price
    - predicted movement = predicted future price - current price
    - direction = up / down / flat

It opens interactive Plotly charts in the browser and does not save project HTML files
unless --save-html is passed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error

from improved_egg_price_forecast import (
    DATA_DIR,
    DEFAULT_CITY,
    DEFAULT_HORIZONS,
    DEFAULT_SPLIT_DATE,
    build_features,
    load_city_data,
    open_plotly_in_browser,
    prediction_column_name,
    train_best_xgb_delta_models,
)


SCRIPT_DIR = Path(__file__).resolve().parent


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


def movement_direction(change: pd.Series, threshold: float) -> pd.Series:
    return pd.Series(
        np.select(
            [change > threshold, change < -threshold],
            ["up", "down"],
            default="flat",
        ),
        index=change.index,
    )


def direction_metrics(frame: pd.DataFrame) -> dict:
    actual = frame["Actual_Direction"]
    predicted = frame["Predicted_Direction"]
    rows = {
        "Direction_Accuracy": float((actual == predicted).mean()),
        "Up_Accuracy": np.nan,
        "Down_Accuracy": np.nan,
        "Flat_Accuracy": np.nan,
    }
    for direction, key in [
        ("up", "Up_Accuracy"),
        ("down", "Down_Accuracy"),
        ("flat", "Flat_Accuracy"),
    ]:
        mask = actual == direction
        if mask.any():
            rows[key] = float((predicted[mask] == direction).mean())
    return rows


def rmse(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def build_trend_result(
    raw_data: pd.DataFrame,
    city: str,
    split_date: pd.Timestamp,
    horizon: int,
    threshold: float,
    random_state: int,
) -> tuple[pd.DataFrame, dict]:
    data = build_features(raw_data, horizon)
    city_data = data[data["City"] == city].copy()
    train_city = city_data[city_data["target_date"] < split_date].copy()
    test_city = city_data[city_data["target_date"] >= split_date].copy()

    if train_city.empty or test_city.empty:
        raise ValueError(f"Not enough train/test rows for city {city!r} and horizon {horizon}.")

    predictions = train_best_xgb_delta_models(
        data, train_city, test_city, split_date, horizon, random_state
    )
    predicted_price = predictions["XGBoost best delta strategy"]

    result = pd.DataFrame(
        {
            "City": test_city["City"].to_numpy(),
            "Feature_Date": test_city["Date"].to_numpy(),
            "Target_Date": test_city["target_date"].to_numpy(),
            "Current_Price": test_city["Price"].to_numpy(),
            "Actual_Price": test_city["target"].to_numpy(),
            "Predicted_Price": predicted_price,
        }
    )
    result["Actual_Change"] = result["Actual_Price"] - result["Current_Price"]
    result["Predicted_Change"] = result["Predicted_Price"] - result["Current_Price"]
    result["Movement_Error"] = result["Actual_Change"] - result["Predicted_Change"]
    result["Abs_Movement_Error"] = result["Movement_Error"].abs()
    result["Actual_Direction"] = movement_direction(result["Actual_Change"], threshold)
    result["Predicted_Direction"] = movement_direction(result["Predicted_Change"], threshold)
    result["Direction_Correct"] = result["Actual_Direction"] == result["Predicted_Direction"]

    metrics = {
        "Horizon": horizon,
        "Movement_MAE": mean_absolute_error(result["Actual_Change"], result["Predicted_Change"]),
        "Movement_RMSE": rmse(result["Actual_Change"], result["Predicted_Change"]),
        "Mean_Actual_Change": result["Actual_Change"].mean(),
        "Mean_Predicted_Change": result["Predicted_Change"].mean(),
        **direction_metrics(result),
    }
    return result, metrics


def make_trend_chart(
    result: pd.DataFrame,
    metrics: dict,
    city: str,
    horizon: int,
    threshold: float,
    output_path: Path | None = None,
) -> None:
    colors = result["Direction_Correct"].map({True: "#22c55e", False: "#ef4444"})

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result["Target_Date"],
            y=result["Actual_Change"],
            mode="lines+markers",
            name="Actual movement",
            line=dict(color="#111827", width=2.5),
            marker=dict(size=5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result["Target_Date"],
            y=result["Predicted_Change"],
            mode="lines+markers",
            name="Predicted movement",
            line=dict(color="#2563eb", width=2),
            marker=dict(size=5),
        )
    )
    fig.add_trace(
        go.Bar(
            x=result["Target_Date"],
            y=result["Movement_Error"],
            name="Movement error",
            marker_color="#f97316",
            opacity=0.42,
            yaxis="y2",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result["Target_Date"],
            y=np.full(len(result), 0),
            mode="markers",
            name="Direction correct/wrong",
            marker=dict(color=colors, size=7, symbol="square"),
            yaxis="y3",
            customdata=np.stack(
                [
                    result["Actual_Direction"],
                    result["Predicted_Direction"],
                    result["Actual_Change"].round(2),
                    result["Predicted_Change"].round(2),
                ],
                axis=-1,
            ),
            hovertemplate=(
                "Target date: %{x|%Y-%m-%d}<br>"
                "Actual direction: %{customdata[0]}<br>"
                "Predicted direction: %{customdata[1]}<br>"
                "Actual movement: %{customdata[2]}<br>"
                "Predicted movement: %{customdata[3]}<extra></extra>"
            ),
        )
    )

    fig.add_hline(y=threshold, line=dict(color="#94a3b8", dash="dash", width=1))
    fig.add_hline(y=-threshold, line=dict(color="#94a3b8", dash="dash", width=1))
    fig.add_hline(y=0, line=dict(color="#64748b", width=1))

    fig.update_layout(
        title=(
            f"{city} {horizon}-day Price Trend Forecast"
            f"<br><sup>Movement MAE {metrics['Movement_MAE']:.2f}, "
            f"RMSE {metrics['Movement_RMSE']:.2f}, "
            f"Direction accuracy {metrics['Direction_Accuracy'] * 100:.1f}% | "
            f"Flat threshold +/-{threshold:.1f}</sup>"
        ),
        xaxis_title="Target date",
        yaxis=dict(title="Price movement"),
        yaxis2=dict(
            title="Movement error",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=True,
            zerolinecolor="#9ca3af",
        ),
        yaxis3=dict(
            overlaying="y",
            visible=False,
            range=[-1, 1],
        ),
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )

    if output_path:
        fig.write_html(output_path, include_plotlyjs="cdn", auto_open=False)
    else:
        open_plotly_in_browser(fig, f"{city}_{horizon}day_trend_forecast")


def print_direction_table(result: pd.DataFrame, rows: int) -> None:
    preview = result[
        [
            "Feature_Date",
            "Target_Date",
            "Current_Price",
            "Actual_Price",
            "Predicted_Price",
            "Actual_Change",
            "Predicted_Change",
            "Movement_Error",
            "Actual_Direction",
            "Predicted_Direction",
            "Direction_Correct",
        ]
    ].head(rows)
    print(preview.round(2).to_string(index=False))


def run(args: argparse.Namespace) -> None:
    raw_data = load_city_data(DATA_DIR)
    split_date = pd.Timestamp(args.split_date)
    horizons = parse_horizons(args.horizons)
    metric_rows = []

    for horizon in horizons:
        result, metrics = build_trend_result(
            raw_data=raw_data,
            city=args.city,
            split_date=split_date,
            horizon=horizon,
            threshold=args.threshold,
            random_state=args.random_state,
        )
        metric_rows.append(metrics)

        print(f"\nCity: {args.city}")
        print(f"Horizon: {horizon} day(s)")
        print(f"Rows: {len(result)}")
        print(
            "Trend metrics: "
            f"MAE={metrics['Movement_MAE']:.3f}, "
            f"RMSE={metrics['Movement_RMSE']:.3f}, "
            f"Direction accuracy={metrics['Direction_Accuracy'] * 100:.1f}%"
        )
        print("\nTrend preview:")
        print_direction_table(result, args.rows)

        output_path = None
        if args.save_html:
            output_path = SCRIPT_DIR / f"{args.city.lower()}_{horizon}day_trend_forecast.html"
        make_trend_chart(result, metrics, args.city, horizon, args.threshold, output_path)
        if output_path:
            print(f"Saved trend chart: {output_path}")
        else:
            print(f"Opened trend chart in browser for horizon {horizon}.")

    summary = pd.DataFrame(metric_rows)
    print("\nAll horizon trend summary:")
    display_columns = [
        "Horizon",
        "Movement_MAE",
        "Movement_RMSE",
        "Direction_Accuracy",
        "Up_Accuracy",
        "Down_Accuracy",
        "Flat_Accuracy",
        "Mean_Actual_Change",
        "Mean_Predicted_Change",
    ]
    print(summary[display_columns].round(3).to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Egg price trend forecast charts")
    parser.add_argument("--city", default=DEFAULT_CITY, help="City to evaluate, e.g. Barwala")
    parser.add_argument(
        "--horizons",
        default="all",
        help="Forecast horizons to run. Use 'all' or comma-separated values like 1,2,3,4.",
    )
    parser.add_argument("--split-date", default=DEFAULT_SPLIT_DATE, help="First target date in test set")
    parser.add_argument("--threshold", type=float, default=5.0, help="Movement threshold for up/down/flat")
    parser.add_argument("--rows", type=int, default=12, help="Rows to print in the preview table")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--save-html", action="store_true", help="Save chart HTML files instead of only opening them")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
