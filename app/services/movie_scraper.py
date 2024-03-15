from bs4 import BeautifulSoup
import requests
from app.interfaces.movie_scraper import IMovieScraper

class WikipediaMovieScraper(IMovieScraper):
    def __init__(self, base_url):
        self.base_url = base_url

    def _get_soup(self, url):
        response = requests.get(self.base_url + url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return BeautifulSoup(response.content, 'lxml')

    def get_movie_list_data(self, table_url):
        soup = self._get_soup(table_url)
        table = soup.find('table', class_='wikitable')
        if not table:
            raise ValueError("Table not found.")
        
        rows = table.find_all('tr')[1:]  # Exclude header row

        movie_list_data = []
        
        for row in rows:
            columns = row.find_all('td')
            film = columns[0]
            film_text = film.get_text(strip=True)
            film_link = film.find('a')['href'] if film.find('a') else None
            year = columns[1].get_text(strip=True)
            awards = columns[2].get_text(strip=True)
            nominations = columns[3].get_text(strip=True)

            movie_list_data.append({
                "title": film_text,
                "link": film_link,
                "year": year,
                "awards": awards,
                "nominations": nominations
            })

        return movie_list_data

    def get_movie_details(self, link):
        soup = self._get_soup(link)
        infobox = soup.find('table', class_='infobox')
        if not infobox:
            raise ValueError("Infobox not found.")

        labels = []
        data = []

        for row in infobox.find_all('tr'):
            references = row.find_all(class_='reference')
            for reference in references:
                reference.extract() # Exclude text inside reference class

            label = row.find(class_='infobox-label')
            data_item = row.find(class_='infobox-data')
            
            if label and data_item:
                labels.append(label.get_text(strip=True))
                if data_item.find('ul'):
                    # Extract list items as a list
                    list_items = [li.get_text(strip=True).replace('\xa0', ' ') for li in data_item.find_all('li')]
                    data.append(list_items)
                else:
                    data.append(data_item.get_text(strip=True).replace('\xa0', ' '))

        return dict(zip(labels, data))
