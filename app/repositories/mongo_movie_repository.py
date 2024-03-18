from app.interfaces.movie_repository import MovieRepository
from app.config.database import db
from bson import ObjectId


class MongoMovieRepository(MovieRepository):
    def __init__(self):
        pass

    def delete_all_movies(self):
        return db.movies.delete_many({})

    def insert_movie(self, movie):
        return db.movies.insert_one(movie)

    def insert_many_movies(self, movies):
        return db.movies.insert_many(movies)

    def get_movie(self, movie_id):
        return db.movies.find_one({'_id': ObjectId(movie_id)})

    def get_all_movies(self, page=1, count=10):
        return db.movies.find().skip((page - 1) * count).limit(count)

    def update_movie(self, movie_id, movie):
        return db.movies.update_one({'_id': ObjectId(movie_id)}, {'$set': movie})
        

    def delete_movie(self, movie_id):
        return db.movies.delete_one({'_id': ObjectId(movie_id)})