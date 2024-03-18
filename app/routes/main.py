from fastapi import APIRouter
from app.routes import movie_routes

api_router = APIRouter()

api_router.include_router(movie_routes.router, prefix="/movies", tags=["movies"])