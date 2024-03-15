from fastapi import APIRouter, HTTPException
from app.config.database import db
from app.dto import movie_dto
from typing import List
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_movies(page: int = 1, count: int = 10) -> List[dict]:
    movies = db.movies.find().skip((page - 1) * count).limit(count)
    return movie_dto.list_response(movies)

@router.get("/{movie_id}")
async def get_movie(movie_id: str) -> dict:
    movie = db.movies.find_one({"_id": ObjectId(movie_id)})
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie_dto.response(movie)