from abc import ABC, abstractmethod

class MovieRepository(ABC):
    @abstractmethod
    def __init__(self, db):
        pass

    @abstractmethod
    def delete_all_movies(self):
        pass

    @abstractmethod
    def insert_movie(self, movie):
        pass

    @abstractmethod
    def insert_many_movies(self, movies):
        pass

    @abstractmethod
    def get_movie(self, movie_id):
        pass

    @abstractmethod
    def get_all_movies(self, page, count):
        pass

    @abstractmethod
    def update_movie(self, movie_id, movie):
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        pass