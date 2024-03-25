from fastapi import APIRouter
from app.api.v1.endpoints import movie

router = APIRouter()

router.include_router(movie.router)