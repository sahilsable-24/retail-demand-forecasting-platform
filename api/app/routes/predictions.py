from fastapi import APIRouter, HTTPException
from api.app.dependencies import stores_df,get_model_artifacts,get_store_history
from demand_forecasting.models.predict import predict_horizon
from api.app.schemas.prediction import PredictionRequest,PredictionResponse,HistoricalSales,PredictedData
import pandas as pd

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if request.store_id not in stores_df["Store"].values:
        raise HTTPException(status_code=404, detail=f"{request.store_id} not found in the stores data")

    if len(request.promo_schedule) != request.horizon_days:
        raise HTTPException(status_code=400,detail="Promo schedule length must match the horizon days")

    model,encoder,feature_cols = get_model_artifacts()
    store_history_df = get_store_history(request.store_id,pd.Timestamp(request.start_date))

    forecast_df = predict_horizon(
        store_history_df=store_history_df,
        model=model,
        encoder=encoder,
        feature_cols=feature_cols,
        start_date=pd.Timestamp(request.start_date),
        horizon_days=request.horizon_days,
        promo_schedule=request.promo_schedule,
        state_holiday_schedule=request.state_holiday_schedule,
        school_holiday_schedule=request.school_holiday_schedule,
        open_schedule=request.open_schedule
    )

    historical = store_history_df.tail(14)[["Date", "Sales"]]

    return PredictionResponse(
        store_id=request.store_id,
        start_date=request.start_date,
        horizon_days=request.horizon_days,
        historical=[HistoricalSales(date=row["Date"],sales=row["Sales"]) for _,row in historical.iterrows()],
        predictions=[PredictedData(date=row["Date"],predicted_sales=round(row["Predicted_Sales"])) for _,row in forecast_df.iterrows()]
    )

