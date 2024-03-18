from app.interfaces.movie_repository import MovieRepository
from bson import ObjectId


class MovieRepository(MovieRepository):
    def __init__(self, db):
        self.db = db

    def delete_all_movies(self):
        return self.db.movies.delete_many({})

    def insert_movie(self, movie):
        return self.db.movies.insert_one(movie)

    def insert_many_movies(self, movies):
        return self.db.movies.insert_many(movies)

    def get_movie(self, movie_id):
        return self.db.movies.find_one({'_id': ObjectId(movie_id)})

    def get_all_movies(self, page=1, count=10):
        return self.db.movies.find().skip((page - 1) * count).limit(count)

    def update_movie(self, movie_id, movie):
        return self.db.movies.update_one({'_id': ObjectId(movie_id)}, {'$set': movie})
        

    def delete_movie(self, movie_id):
        return self.db.movies.delete_one({'_id': ObjectId(movie_id)})