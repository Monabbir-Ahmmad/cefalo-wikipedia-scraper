from app.core.factory import AppFactory


def main():
    app_factory = AppFactory()

    movie_scraper_service = app_factory.movie_scraper_service

    movie_details_list = movie_scraper_service.scrape_all_movie_details('/wiki/List_of_Academy_Award–winning_films')
    movie_scraper_service.insert_movie_details_to_db(movie_details_list)
    movie_scraper_service.insert_movie_rating()

if __name__ == '__main__':
    main()