import sys
from pathlib import Path
from datetime import timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

try:
    from xgboost import XGBRegressor
except ImportError as exc:
    raise ImportError(
        "XGBoost is required. Install it with: pip install xgboost"
    ) from exc


sys.stdout.reconfigure(line_buffering=True)


FEATURES = [
    "market_rating",
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


def daily_market_rating(change):
    """Same rating logic used in feature_extraction.py."""
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


def _clean_main_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    if "is_festival" not in df.columns:
        df["is_festival"] = 0
    else:
        df["is_festival"] = df["is_festival"].notna().astype(int)

    for column in ["Price", "market_rating", "tmax", "prcp"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def load_data(csv_path):
    """
    Load and clean the egg price data.
    
    Args:
        csv_path: Path to the CSV file
    
    Returns:
        Cleaned DataFrame with Date and Price columns
    """
    df = pd.read_csv(csv_path)
    df = _clean_main_data(df)
    return df


def split_train_test_dynamic(df, test_period_days=365):
    """
    Dynamically split data into training and test sets based on the latest date.
    
    NO HARDCODED YEARS - This works for any dataset update automatically.
    
    Args:
        df: Cleaned DataFrame with Date column
        test_period_days: Number of days for test period (default: 365 days = 1 year)
    
    Returns:
        Tuple of (train_df, test_df)
        - train_df: All records older than test_period_days from latest date
        - test_df: Last test_period_days of data
    """
    # Get the maximum (latest) date in the dataset
    max_date = df["Date"].max()
    
    # Calculate the test start date: latest_date - test_period_days
    test_start_date = max_date - timedelta(days=test_period_days)
    
    # Split: training = everything before test_start_date, test = test_start_date onwards
    train_df = df[df["Date"] < test_start_date].copy()
    test_df = df[df["Date"] >= test_start_date].copy()
    
    print(f"\n{'='*70}", flush=True)
    print(f"DYNAMIC TRAIN/TEST SPLIT (based on latest date: {max_date.date()})", flush=True)
    print(f"{'='*70}", flush=True)
    print(f"Training period:   {train_df['Date'].min().date()} to {train_df['Date'].max().date()}", flush=True)
    print(f"Test period:       {test_df['Date'].min().date()} to {test_df['Date'].max().date()}", flush=True)
    print(f"Training samples:  {len(train_df)}", flush=True)
    print(f"Test samples:      {len(test_df)}", flush=True)
    print(f"{'='*70}\n", flush=True)
    
    return train_df, test_df


def train_price_model(train_df):
    """
    Train the XGBoost model on the training dataset only.
    
    Args:
        train_df: DataFrame containing training data with all required features
    
    Returns:
        Trained XGBRegressor model
    
    Raises:
        ValueError: If insufficient training data available
    """
    model_data = train_df[["Date", "Price"] + FEATURES].dropna().reset_index(drop=True)

    if len(model_data) < 60:
        raise ValueError(f"Need at least 60 rows after dropping missing values. Got {len(model_data)}")

    x_train = model_data[FEATURES]
    y_train = model_data["Price"]

    print(f"Training model on {len(x_train)} samples...", flush=True)
    
    model = XGBRegressor(
        objective="reg:squarederror",
        eval_metric="rmse",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
        n_estimators=500,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
    )
    model.fit(x_train, y_train)
    return model


def _historical_value(df, date, column, default_value=0):
    """Get historical value for a date from the same day/month/year or median."""
    same_day = df[(df["Date"].dt.month == date.month) & (df["Date"].dt.day == date.day)]
    if same_day[column].notna().any():
        return float(same_day[column].median())

    same_month = df[df["Date"].dt.month == date.month]
    if same_month[column].notna().any():
        return float(same_month[column].median())

    if df[column].notna().any():
        return float(df[column].median())

    return default_value


def _future_feature_value(df, future_features, date, column, default_value=0):
    """Get feature value from future_features or fall back to historical value."""
    if future_features is not None and column in future_features.columns:
        matches = future_features[future_features["Date"] == date]
        if not matches.empty and pd.notna(matches.iloc[0][column]):
            return float(matches.iloc[0][column])

    return _historical_value(df, date, column, default_value=default_value)


def _build_next_row(history, base_df, forecast_date, future_features=None):
    prices = history["Price"].astype(float)
    previous_price = float(prices.iloc[-1])
    previous_previous_price = float(prices.iloc[-2]) if len(prices) >= 2 else previous_price
    previous_change = ((previous_price - previous_previous_price) / previous_previous_price) * 100

    row = {
        "Date": forecast_date,
        "market_rating": daily_market_rating(previous_change),
        "lag_3": float(prices.iloc[-3]),
        "lag_7": float(prices.iloc[-7]),
        "lag_14": float(prices.iloc[-14]),
        "lag_30": float(prices.iloc[-30]),
        "rolling_mean_7": float(prices.tail(7).mean()),
        "rolling_mean_14": float(prices.tail(14).mean()),
        "rolling_mean_30": float(prices.tail(30).mean()),
        "rolling_std_7": float(prices.tail(7).std()),
        "tmax": _future_feature_value(base_df, future_features, forecast_date, "tmax"),
        "prcp": _future_feature_value(base_df, future_features, forecast_date, "prcp"),
        "dayofweek": forecast_date.dayofweek,
        "weekofyear": int(forecast_date.isocalendar().week),
        "quarter": forecast_date.quarter,
        "is_weekend": int(forecast_date.dayofweek in [5, 6]),
        "is_festival": int(_future_feature_value(base_df, future_features, forecast_date, "is_festival")),
    }
    return row


def recursive_forecast(
    train_df,
    test_df,
    base_df,
    model=None,
    future_features=None,
):
    """
    Perform recursive (multi-step ahead) forecasting on the test period.
    
    IMPORTANT: This is TRUE recursive forecasting - no data leakage!
    - Each prediction uses ONLY historical data and previously predicted values
    - At step t, we use prices up to step t-1 (mixing actual training data and predictions)
    - We NEVER use actual test values during prediction (no cheating!)
    - This simulates real forecasting where future actual values are unknown
    
    Args:
        train_df: Training dataset used to train the model
        test_df: Test dataset with actual prices (used only for comparison, never for features)
        base_df: Full dataset for historical feature lookups (for weather, festival features)
        model: Trained XGBRegressor model (if None, trains on train_df)
        future_features: DataFrame with future features (weather, festivals)
    
    Returns:
        DataFrame with columns: Date, Actual_Price, Predicted_Price
    """
    print(f"\nStarting recursive forecasting for {len(test_df)} days...", flush=True)
    
    # Train model if not provided
    if model is None:
        model = train_price_model(train_df)
    
    # Initialize history with training data prices (this is what the model "knows")
    history = train_df[["Date", "Price"]].dropna().sort_values("Date").reset_index(drop=True)
    
    if len(history) < 30:
        raise ValueError("Need at least 30 historical prices for recursive forecasting.")
    
    # Prepare future features if provided
    if future_features is not None:
        future_features = future_features.copy()
        future_features["Date"] = pd.to_datetime(future_features["Date"])
    
    forecasts = []
    
    # Recursively forecast each day in the test period
    for idx, (test_idx, test_row) in enumerate(test_df.iterrows(), 1):
        test_date = pd.Timestamp(test_row["Date"])
        actual_price = float(test_row["Price"])
        
        # Build features using ONLY historical/predicted data (no actual test data)
        # This is the key to avoiding data leakage
        feature_row = _build_next_row(history, base_df, test_date, future_features)
        
        # Make prediction
        predicted_price = float(model.predict(pd.DataFrame([feature_row])[FEATURES])[0])
        
        # Store results
        forecasts.append({
            "Date": test_date,
            "Actual_Price": actual_price,
            "Predicted_Price": predicted_price,
        })
        
        # CRUCIAL: Add predicted price to history for NEXT iteration
        # This is recursive forecasting - we use our prediction as input for the next step
        # We do NOT add the actual price here (that would be cheating / data leakage)
        history = pd.concat(
            [
                history,
                pd.DataFrame([{"Date": test_date, "Price": predicted_price}]),
            ],
            ignore_index=True,
        )
        
        if idx % 50 == 0 or idx == len(test_df):
            print(f"  Forecast progress: {idx}/{len(test_df)} days completed", flush=True)
    
    result_df = pd.DataFrame(forecasts)
    print(f"Recursive forecasting completed!\n", flush=True)
    
    return result_df


def evaluate_forecast(forecast_df):
    """
    Calculate evaluation metrics for the forecast.
    
    Args:
        forecast_df: DataFrame with Actual_Price and Predicted_Price columns
    
    Returns:
        Dictionary with evaluation metrics
    """
    y_actual = forecast_df["Actual_Price"].values
    y_pred = forecast_df["Predicted_Price"].values
    
    # Calculate metrics
    mae = mean_absolute_error(y_actual, y_pred)
    rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
    r2 = r2_score(y_actual, y_pred)
    mape = np.mean(np.abs((y_actual - y_pred) / y_actual)) * 100
    
    metrics = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "MAPE": mape,
    }
    
    print(f"\n{'='*70}", flush=True)
    print(f"FORECAST EVALUATION METRICS", flush=True)
    print(f"{'='*70}", flush=True)
    print(f"MAE  (Mean Absolute Error):           {mae:.2f} ₹", flush=True)
    print(f"RMSE (Root Mean Squared Error):       {rmse:.2f} ₹", flush=True)
    print(f"R²   (Coefficient of Determination): {r2:.4f}", flush=True)
    print(f"MAPE (Mean Absolute Percentage Error): {mape:.2f}%", flush=True)
    print(f"{'='*70}\n", flush=True)
    
    return metrics


def visualize_forecast_interactive(forecast_df, output_html_path=None):
    """
    Create an interactive Plotly Express visualization of actual vs predicted prices.
    Automatically opens in browser using fig.show().
    
    Args:
        forecast_df: DataFrame with Date, Actual_Price, Predicted_Price columns
        output_html_path: Optional path to save the HTML file
    
    Returns:
        Plotly Figure object
    """
    # Sort by date for proper line visualization
    plot_df = forecast_df[["Date", "Actual_Price", "Predicted_Price"]].copy()
    plot_df = plot_df.sort_values("Date").reset_index(drop=True)
    
    # Create interactive figure with Plotly Graph Objects for more control
    fig = go.Figure()
    
    # Add actual price trace
    fig.add_trace(go.Scatter(
        x=plot_df["Date"],
        y=plot_df["Actual_Price"],
        mode="lines",
        name="Actual Price",
        line=dict(color="rgb(31, 119, 180)", width=2.5),
        hovertemplate="<b>Actual Price</b><br>Date: %{x|%Y-%m-%d}<br>Price: ₹%{y:.2f}<extra></extra>",
    ))
    
    # Add predicted price trace
    fig.add_trace(go.Scatter(
        x=plot_df["Date"],
        y=plot_df["Predicted_Price"],
        mode="lines",
        name="Predicted Price",
        line=dict(color="rgb(255, 127, 14)", width=2.5, dash="dash"),
        hovertemplate="<b>Predicted Price</b><br>Date: %{x|%Y-%m-%d}<br>Price: ₹%{y:.2f}<extra></extra>",
    ))
    
    # Update layout with professional styling
    fig.update_layout(
        title={
            "text": "Recursive Egg Price Forecast vs Actual",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20}
        },
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode="x unified",
        template="plotly_white",
        height=700,
        width=1400,
        font=dict(size=12, family="Arial"),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor="rgba(100, 100, 100, 0.5)",
            borderwidth=1,
            font=dict(size=11)
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(200, 200, 200, 0.3)",
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(200, 200, 200, 0.3)",
        ),
    )
    
    # Save to HTML if path provided
    if output_html_path:
        output_html_path = Path(output_html_path)
        output_html_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_html_path))
        print(f"Interactive plot saved: {output_html_path}", flush=True)
    
    # Auto-open in browser
    print("Opening interactive visualization in browser...", flush=True)
    fig.show(renderer="browser")
    
    return fig


def forecast_next_year(
    csv_path,
    periods=365,
    model=None,
    future_features=None,
    output_path=None,
):
    """
    Recursively forecast prices.

    Day 1 uses historical lags. Day 2 uses the Day 1 predicted price in its
    lag/rolling features. This continues until `periods` days are predicted.
    """
    csv_path = Path(csv_path)
    df = _clean_main_data(pd.read_csv(csv_path))

    if future_features is not None:
        future_features = future_features.copy()
        future_features["Date"] = pd.to_datetime(future_features["Date"])

    model = model or train_price_model(df)

    history = df[["Date", "Price"]].dropna().sort_values("Date").reset_index(drop=True)
    if len(history) < 30:
        raise ValueError("Need at least 30 historical prices for recursive forecasting.")

    forecasts = []
    next_date = history["Date"].max() + pd.Timedelta(days=1)

    for step in range(1, periods + 1):
        feature_row = _build_next_row(history, df, next_date, future_features)
        predicted_price = float(model.predict(pd.DataFrame([feature_row])[FEATURES])[0])

        forecast_row = {
            **feature_row,
            "Predicted_Price": predicted_price,
            "Step": step,
        }
        forecasts.append(forecast_row)

        history = pd.concat(
            [
                history,
                pd.DataFrame([{"Date": next_date, "Price": predicted_price}]),
            ],
            ignore_index=True,
        )
        next_date = next_date + pd.Timedelta(days=1)

    forecast_df = pd.DataFrame(forecasts)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        forecast_df.to_csv(output_path, index=False)
        print(f"Forecast saved: {output_path}", flush=True)

    return forecast_df


if __name__ == "__main__":
    # ======================================================================
    # MAIN EXECUTION PIPELINE
    # ======================================================================
    
    # Configuration
    data_path = r"D:\egg_price_procject\output\main_data\Barwala_main_data.csv"
    output_csv_path = r"D:\egg_price_procject\output\forecast\recursive_predictions_test_period.csv"
    output_html_path = r"D:\egg_price_procject\analysis\analysis_chart\recursive_forecast_interactive.html"
    
    try:
        # Step 1: Load and clean the data
        print("\n" + "="*70, flush=True)
        print("STEP 1: LOADING AND PREPARING DATA", flush=True)
        print("="*70, flush=True)
        df = load_data(data_path)
        print(f"Data loaded: {len(df)} records from {data_path}", flush=True)
        print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}", flush=True)
        
        # Step 2: Dynamically split into train and test (no hardcoded years!)
        print("\n" + "="*70, flush=True)
        print("STEP 2: DYNAMIC TRAIN/TEST SPLIT", flush=True)
        print("="*70, flush=True)
        train_df, test_df = split_train_test_dynamic(df, test_period_days=365)
        
        # Validate data
        if len(train_df) < 60:
            raise ValueError(f"Not enough training data: {len(train_df)} samples (need >= 60)")
        if len(test_df) < 30:
            raise ValueError(f"Not enough test data: {len(test_df)} samples (need >= 30)")
        
        # Step 3: Train the model on training data only
        print("\n" + "="*70, flush=True)
        print("STEP 3: MODEL TRAINING", flush=True)
        print("="*70, flush=True)
        model = train_price_model(train_df)
        print("Model training completed successfully!", flush=True)
        
        # Step 4: Perform recursive forecasting on test period
        print("\n" + "="*70, flush=True)
        print("STEP 4: RECURSIVE FORECASTING", flush=True)
        print("="*70, flush=True)
        forecast_results = recursive_forecast(
            train_df=train_df,
            test_df=test_df,
            base_df=df,
            model=model,
            future_features=None,  # Set to a DataFrame if weather/festival features available
        )
        
        # Step 5: Evaluate the forecast
        print("\n" + "="*70, flush=True)
        print("STEP 5: EVALUATION", flush=True)
        print("="*70, flush=True)
        metrics = evaluate_forecast(forecast_results)
        
        # Step 6: Save results to CSV
        print("\n" + "="*70, flush=True)
        print("STEP 6: SAVING RESULTS", flush=True)
        print("="*70, flush=True)
        output_csv_path = Path(output_csv_path)
        output_csv_path.parent.mkdir(parents=True, exist_ok=True)
        forecast_results.to_csv(output_csv_path, index=False)
        print(f"Prediction results saved: {output_csv_path}", flush=True)
        print(f"\nResults CSV content (first 5 rows):")
        print(forecast_results.head(), flush=True)
        print(f"\nResults CSV content (last 5 rows):")
        print(forecast_results.tail(), flush=True)
        
        # Step 7: Create interactive visualization and open in browser
        print("\n" + "="*70, flush=True)
        print("STEP 7: VISUALIZATION", flush=True)
        print("="*70, flush=True)
        fig = visualize_forecast_interactive(forecast_results, output_html_path=output_html_path)
        
        # Final summary
        print("\n" + "="*70, flush=True)
        print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!", flush=True)
        print("="*70, flush=True)
        print(f"✓ Train period: {train_df['Date'].min().date()} to {train_df['Date'].max().date()}", flush=True)
        print(f"✓ Test period:  {test_df['Date'].min().date()} to {test_df['Date'].max().date()}", flush=True)
        print(f"✓ Metrics: MAE={metrics['MAE']:.2f}, RMSE={metrics['RMSE']:.2f}, R²={metrics['R2']:.4f}, MAPE={metrics['MAPE']:.2f}%", flush=True)
        print(f"✓ Results saved: {output_csv_path}", flush=True)
        print(f"✓ Chart saved:   {output_html_path}", flush=True)
        print(f"✓ Opening interactive visualization in browser...", flush=True)
        print("="*70 + "\n", flush=True)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
