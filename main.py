from fastapi import FastAPI
from app.routes.main import api_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/api/v1")