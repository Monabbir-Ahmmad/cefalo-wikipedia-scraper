from app.interfaces.movie_repository import MovieRepository
from bson import ObjectId

class MongoMovieRepository(MovieRepository):
    def __init__(self, db):
        self.db = db

    def delete_all_movies(self):
        return self.db.movies.delete_many({})

    def insert_movie(self, movie):
        return self.db.movies.insert_one(movie)

    def insert_many_movies(self, movies):
        return self.db.movies.insert_many(movies)

    def get_movie(self, movie_id):
        pipeline = [
            {"$match": {"_id": movie_id}},
            {
                "$addFields": {
                    "averageRating": {"$avg": "$ratings.rating"},
                    "ratingsCount": {"$size": "$ratings"},
                }
            },
        ]
        result = list(self.db.movies.aggregate(pipeline))
        return result[0] if result else None

    def get_all_movies(self, page=1, count=10):
        return self.db.movies.aggregate(
            [
                {"$skip": (page - 1) * count},
                {"$limit": count},
                {
                    "$addFields": {
                        "averageRating": {"$avg": "$ratings.rating"},
                        "ratingsCount": {"$size": "$ratings"},
                    }
                },
            ]
        )

    def update_movie(self, movie_id, movie):
        return self.db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": movie})

    def delete_movie(self, movie_id):
        return self.db.movies.delete_one({"_id": ObjectId(movie_id)})