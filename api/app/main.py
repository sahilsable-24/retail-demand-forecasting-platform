from fastapi import FastAPI
from api.app.routes import stores,predictions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(stores.router)

app.include_router(predictions.router)