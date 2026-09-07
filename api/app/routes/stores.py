from fastapi import APIRouter
from api.app.dependencies import get_stores

router = APIRouter()

@router.get("/stores")
def list_stores():
    stores_df = get_stores()
    return stores_df.to_dict(orient="records")