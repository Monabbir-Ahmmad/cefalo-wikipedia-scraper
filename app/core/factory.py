from app.services.wikipedia_movie_scraper import WikipediaMovieScraper
from app.repositories.mongo.mongo_movie_repository import MongoMovieRepository
from app.services.movie_scraper_service import MovieDetailsScraperService
from app.services.movie_service import MovieService
from app.utils.decorator import singleton
from app.core.database import Database
from app.core.config import Config

@singleton
class AppFactory:
    def __init__(self):
        self.db = Database(Config.MONGODB_URI).create()
        self.scraper = WikipediaMovieScraper('https://en.wikipedia.org')
        self.movie_repository = MongoMovieRepository(self.db)
        self.movie_service = MovieService(self.movie_repository)
        self.movie_scraper_service = MovieDetailsScraperService(self.scraper, self.movie_service)

        print("App factory created")