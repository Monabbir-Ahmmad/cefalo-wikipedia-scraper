from abc import ABC, abstractmethod

class IMovieScraper(ABC):
    @abstractmethod
    def __init__(self, base_url):
        pass

    @abstractmethod
    def get_movie_list_data(self, table_url):
        pass

    @abstractmethod
    def get_movie_details(self, link):
        pass