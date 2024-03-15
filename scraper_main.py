import json
from concurrent.futures import ThreadPoolExecutor
from app.interfaces.movie_scraper import IMovieScraper
from app.services.movie_scraper import WikipediaMovieScraper
from app.config.database import db

class MovieDetailsScraperService:
    def __init__(self, scraper: IMovieScraper):
        self.scraper = scraper

    def scrape_movie_details(self, movie):
        try:
            movie_details = self.scraper.get_movie_details(movie['link'])
            movie_details = {k.lower().replace(' ', '_'): v for k, v in movie_details.items()}
            movie.update(movie_details)

            print(f"Movie '{movie['title']}' details scraped successfully!")

        except Exception as e:
            print(f"Error occurred while scraping movie '{movie['title']}' details: {e}")

        return movie

    def scrape_all_movie_details(self, list_url):
        movie_table_data = self.scraper.get_movie_list_data(list_url)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.scrape_movie_details, movie) for movie in movie_table_data]
            movie_details_list = [future.result() for future in futures]

        return movie_details_list

    def save_movie_details_to_file(self, movie_details_list):
        with open('movie_details.json', 'w') as file:
            json.dump(movie_details_list, file, indent=4)

        print("Data saved to 'movie_details.json' successfully!")

    def insert_movie_details_to_db(self):
        with open('movie_details.json', 'r') as file:
            movie_details_list = json.load(file)

        db.movies.insert_many(movie_details_list)
        
        print("Data inserted into MongoDB successfully!")


if __name__ == '__main__':
    base_url = 'https://en.wikipedia.org'
    scraper = WikipediaMovieScraper(base_url)
    movie_details_service = MovieDetailsScraperService(scraper)

    movie_details_list = movie_details_service.scrape_all_movie_details('/wiki/List_of_Academy_Award–winning_films')
    movie_details_service.save_movie_details_to_file(movie_details_list)
    movie_details_service.insert_movie_details_to_db()
