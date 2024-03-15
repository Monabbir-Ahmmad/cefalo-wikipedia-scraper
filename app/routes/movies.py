from fastapi import APIRouter, HTTPException
from app.config.database import db
from app.dto import movie_dto
from typing import List
from bson import ObjectId
from app.models.movie import MovieModel

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

@router.post("/")
async def create_movie(movie: MovieModel) -> dict:
    result = db.movies.insert_one(movie)
    movie["_id"] = str(result.inserted_id)
    return movie_dto.response(movie)

@router.put("/{movie_id}")
async def update_movie(movie_id: str, movie: MovieModel) -> dict:
    result = db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": movie})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie = db.movies.find_one({"_id": ObjectId(movie_id)})
    
    return movie_dto.response(movie)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: str) -> dict:
    result = db.movies.delete_one({"_id": ObjectId(movie_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"message": f"Movie with id {movie_id} has been deleted"}