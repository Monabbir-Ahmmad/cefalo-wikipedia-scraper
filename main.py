from scraper import WikipediaScraper


base_url = 'https://en.wikipedia.org'
scraper = WikipediaScraper(base_url)
table_data = scraper.scrap_movie_table('/wiki/List_of_Academy_Award–winning_films')
print(table_data)

movie_details = scraper.scrap_movie_details(table_data[0]['Link'])

print(movie_details)