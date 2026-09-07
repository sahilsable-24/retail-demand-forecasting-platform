from pydantic import BaseModel
from datetime import date
from typing import Optional

class PredictionRequest(BaseModel):
    store_id: int
    start_date: date
    horizon_days: int
    promo_schedule: list[int]
    state_holiday_schedule: Optional[list[str]] = None
    school_holiday_schedule: Optional[list[int]] = None
    open_schedule: Optional[list[int]] = None

class HistoricalSales(BaseModel):
    date: date
    sales: int

class PredictedData(BaseModel):
    date: date
    predicted_sales: int

class PredictionResponse(BaseModel):
    store_id: int
    start_date: date
    horizon_days: int
    historical: list[HistoricalSales]
    predictions: list[PredictedData]