import pandas as pd
import numpy as np
import joblib
from demand_forecasting.config.settings import ARTIFACT_DIR


def load_model_and_encoder_feature_cols():
    model_path = ARTIFACT_DIR/"random_forest_model.pkl"
    encoder_path = ARTIFACT_DIR/"one_hot_encoder.pkl"
    feature_cols_path = ARTIFACT_DIR/"feature_cols.pkl"
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    feature_cols = joblib.load(feature_cols_path)
    return model,encoder,feature_cols

def predict_single_day(store_history_df,model,encoder,feature_cols,target_date,promo=0,state_holiday="0",school_holiday=0):
    sales_lag_1 = store_history_df['Sales'].iloc[-1]
    sales_roll_mean_2 = store_history_df['Sales'].tail(2).mean()
    sales_roll_mean_7 = store_history_df["Sales"].tail(7).mean()

    day_of_week = target_date.dayofweek + 1
    month = target_date.month

    store_id = store_history_df["Store"].iloc[0]

    encoded_val = encoder.transform(pd.DataFrame({'StateHoliday': [state_holiday]}))[0]

    features = {
        'Store': store_id,
        'DayOfWeek': day_of_week,
        'Month': month,
        'Promo': promo,
        'SchoolHoliday': school_holiday,
        'sales_lag_1': sales_lag_1,
        'sales_roll_mean_2': sales_roll_mean_2,
        'sales_roll_mean_7': sales_roll_mean_7,
        'StateHoliday_0': encoded_val[0],
        'StateHoliday_a': encoded_val[1],
        'StateHoliday_b': encoded_val[2],
        'StateHoliday_c': encoded_val[3]
    }

    X_pred = pd.DataFrame([features])
    X_pred = X_pred[feature_cols]

    predictions = model.predict(X_pred)[0]

    return predictions

def predict_horizon(store_history_df, model,encoder, feature_cols, start_date,horizon_days,promo_schedule,state_holiday_schedule=None, school_holiday_schedule=None,open_schedule=None):
    current_history = store_history_df.copy()
    results= []
    if state_holiday_schedule is None:
        state_holiday_schedule = ['0'] * horizon_days

    if school_holiday_schedule is None:
        school_holiday_schedule = [0] * horizon_days

    if open_schedule is None:
        open_schedule = [1] * horizon_days

    for i in range(horizon_days):
        target_date = start_date + pd.Timedelta(days=i)

        if open_schedule[i] == 0:
            prediction = 0.0
        else:
            prediction = predict_single_day(current_history,model,encoder,feature_cols,target_date,promo_schedule[i],state_holiday_schedule[i],school_holiday_schedule[i])

        new_row = pd.DataFrame({
            "Store":[current_history['Store'].iloc[0]],
            "Date": [target_date],
            "Sales": [prediction]
        })

        current_history = pd.concat([current_history, new_row], ignore_index=True)

        results.append({"Date": target_date, "Predicted_Sales":prediction})

    return pd.DataFrame(results)