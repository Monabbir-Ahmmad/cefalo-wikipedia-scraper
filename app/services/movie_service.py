from app.interfaces.movie_service import MovieService
from app.interfaces.movie_repository import MovieRepository
from app.dto import movie_dto

class MovieService(MovieService):
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def delete_all_movies(self):
        return self.movie_repository.delete_all_movies()

    def create_movie(self, movie):
        result =  self.movie_repository.insert_movie(movie)
        movie["_id"] = str(result.inserted_id)
        return movie_dto.response(movie)

    def create_many_movies(self, movies):
        return self.movie_repository.insert_many_movies(movies)

    def get_movie(self, movie_id):
        movie =  self.movie_repository.get_movie(movie_id)

        if movie is None:
            return None
        
        return movie_dto.response(movie)

    def get_all_movies(self, page=1, count=10):
        movies = self.movie_repository.get_all_movies(page, count)
        return movie_dto.list_response(movies)

    def update_movie(self, movie_id, movie):
        result = self.movie_repository.update_movie(movie_id, movie)
        if result == 0:
            return None
        
        return self.get_movie(movie_id)

    def delete_movie(self, movie_id):
        return self.movie_repository.delete_movie(movie_id)