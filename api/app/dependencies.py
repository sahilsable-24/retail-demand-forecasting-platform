from demand_forecasting.config.settings import DATA_DIR_RAW
from demand_forecasting.models.predict import load_model_and_encoder_feature_cols
import pandas as pd

stores_df = pd.read_csv(DATA_DIR_RAW/"store.csv")
stores_df = stores_df.astype(object).where(pd.notnull(stores_df), None)

# print(stores_df)

sales_df = pd.read_csv(DATA_DIR_RAW/"train.csv", dtype={'StateHoliday': str})
sales_df["Date"] = pd.to_datetime(sales_df["Date"])

model, encoder, feature_cols = load_model_and_encoder_feature_cols()

def get_stores():
    return stores_df

def get_store_history(store_id,before_date):
    history = sales_df[(sales_df["Store"] == store_id) & (sales_df["Date"]<before_date)]
    return history.sort_values('Date')

def get_model_artifacts():
    return model,encoder,feature_cols

