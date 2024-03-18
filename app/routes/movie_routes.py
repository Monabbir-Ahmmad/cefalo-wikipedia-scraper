from fastapi import APIRouter, HTTPException
from app.config.database import db
from app.dto import movie_dto
from typing import List
from app.schemas.movie import MovieSchema
from factory import AppFactory

app_factory = AppFactory()

movie_service = app_factory.movie_service

router = APIRouter()

@router.get("/")
async def get_movies(page: int = 1, count: int = 10) -> List[dict]:
    movies = movie_service.get_all_movies(page, count)
    return movie_dto.list_response(movies)

@router.get("/{movie_id}")
async def get_movie(movie_id: str) -> dict:
    movie = movie_service.get_movie(movie_id)
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie_dto.response(movie)

@router.post("/")
async def create_movie(movie: MovieSchema) -> dict:
    return movie_service.create_movie(movie)

@router.put("/{movie_id}")
async def update_movie(movie_id: str, movie: MovieSchema) -> dict:
    result = movie_service.update_movie(movie_id, movie)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return result

@router.delete("/{movie_id}")
async def delete_movie(movie_id: str) -> dict:
    result = movie_service.delete_movie(movie_id)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"message": f"Movie with id {movie_id} has been deleted"}

@router.get("/search/{search_term}")
async def search_movies(search_term: str) -> List[dict]:
    movies = movie_service.search_movies(search_term)
    return movie_dto.list_response(movies)