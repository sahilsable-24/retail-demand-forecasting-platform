from fastapi import FastAPI
from api.app.routes import stores,predictions

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(stores.router)

app.include_router(predictions.router)