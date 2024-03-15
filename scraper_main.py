import json
from concurrent.futures import ThreadPoolExecutor
from app.interfaces.movie_scraper import IMovieScraper
from app.services.movie_scraper import WikipediaMovieScraper

def scrape_movie_details(scraper: IMovieScraper, movie):
    try:
        movie_details = scraper.get_movie_details(movie['link'])
        movie_details = {k.lower().replace(' ', '_'): v for k, v in movie_details.items()}
        movie.update(movie_details)

        print(f"Movie '{movie['title']}' details scraped successfully!")
    except Exception as e:
        print(f"Error occurred while scraping movie '{movie['title']}' details: {e}")

    return movie

def scrape_all_movie_details(scraper: IMovieScraper):
    movie_table_data = scraper.get_movie_list_data('/wiki/List_of_Academy_Award–winning_films')

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_movie_details, scraper, movie) for movie in movie_table_data]
        
        movie_details_list = [future.result() for future in futures]
        for future in futures:
            movie = future.result()
            movie_details_list.append(movie)

    return movie_details_list

def save_movie_details_to_file(movie_details_list):
    with open('movie_details.json', 'w') as file:
        json.dump(movie_details_list, file, indent=4)
    print("Data saved to 'movie_details.json' successfully!")

def main():
    base_url = 'https://en.wikipedia.org'
    scraper = WikipediaMovieScraper(base_url)
    
    movie_details_list = scrape_all_movie_details(scraper)
    save_movie_details_to_file(movie_details_list)

if __name__ == '__main__':
    main()
