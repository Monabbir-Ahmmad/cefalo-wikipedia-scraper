from app.services.wikipedia_movie_scraper import WikipediaMovieScraper
from app.repositories.mongo_movie_repository import MongoMovieRepository
from app.services.movie_scraper_service import MovieDetailsScraperService
from app.services.movie_service import MovieService

class AppFactory:
    def __init__(self):
        self.scraper = WikipediaMovieScraper('https://en.wikipedia.org')
        self.movie_repository = MongoMovieRepository()
        self.movie_service = MovieService(self.movie_repository)
        self.movie_scraper_service = MovieDetailsScraperService(self.scraper, self.movie_service)