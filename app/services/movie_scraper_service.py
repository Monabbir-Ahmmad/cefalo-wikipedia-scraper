import pandas as pd
import sys
from concurrent.futures import ThreadPoolExecutor
from app.interfaces.movie_scraper import MovieScraper
from app.interfaces.movie_service import MovieService


class MovieDetailsScraperService:
    def __init__(self, scraper: MovieScraper, movie_service: MovieService):
        self.scraper = scraper
        self.movie_service = movie_service

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

    def insert_movie_details_to_db(self, movie_details_list):
        self.movie_service.delete_all_movies()
        self.movie_service.create_many_movies(movie_details_list)
        print("Data inserted into MongoDB successfully!")

    def _get_movie_list_with_ratings(self):
        movie_details = self.movie_service.get_all_movies(1, sys.maxsize)
        movie_details_df = pd.DataFrame(list(movie_details))
        movies_df = pd.read_csv('data/movies.csv')
        rating_df = pd.read_csv('data/ratings.csv')

        rating_df["userId"] = rating_df["userId"].astype('Int64')
        rating_df["timestamp"] = rating_df["timestamp"].astype('Int64')

        # Extract year from title and clean title
        movies_df["year"] = movies_df["title"].str.extract(r"\((\d{4})\)", expand=True).astype('Int64')
        movies_df["title"] = movies_df["title"].str.replace(r'\s*\(\d{4}\)', '', regex=True).str.strip()

        movies_with_ratings = movies_df.merge(rating_df, on='movieId', how='left')

        movie_details_df['ratings'] = [[] for _ in range(len(movie_details_df))]

        for index, row in movie_details_df.iterrows():
            movie_title = row['title']
            movie_year = row['year']
            
            movie_ratings = movies_with_ratings[(movies_with_ratings['title'] == movie_title) & (movies_with_ratings['year'] == movie_year)][['rating', 'userId', 'timestamp']]
            
            movie_details_df.at[index, 'ratings'] = movie_ratings.to_dict(orient='records')

        movie_details_list = [{k: v for k, v in movie.items() if isinstance(v, list) or pd.notnull(v)} for movie in movie_details_df.to_dict(orient='records')]

        return movie_details_list
    
    def insert_movie_rating(self):
        movie_list_with_ratings = self._get_movie_list_with_ratings()
        self.insert_movie_details_to_db(movie_list_with_ratings)