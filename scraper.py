from bs4 import BeautifulSoup
import requests

class WikipediaScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def _get_soup(self, url):
        response = requests.get(self.base_url + url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return BeautifulSoup(response.content, 'lxml')

    def scrap_movie_table(self, table_url):
        soup = self._get_soup(table_url)
        table = soup.find('table', class_='wikitable')
        if not table:
            raise ValueError("Table not found.")

        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        if headers[:4] != ["Film", "Year", "Awards", "Nominations"]:
            raise ValueError("Table headers do not match.")
        
        rows = table.find_all('tr')[1:]  # Exclude header row

        table_data = []
        for row in rows:
            columns = row.find_all('td')
            film = columns[0]
            film_text = film.get_text(strip=True)
            film_link = film.find('a')['href'] if film.find('a') else None
            year = columns[1].get_text(strip=True)
            awards = columns[2].get_text(strip=True)
            nominations = columns[3].get_text(strip=True)

            table_data.append({
                "Title": film_text,
                "Link": film_link,
                "Year": year,
                "Awards": awards,
                "Nominations": nominations
            })

        return table_data

    def scrap_movie_details(self, link):
        soup = self._get_soup(link)
        infobox = soup.find('table', class_='infobox')
        if not infobox:
            raise ValueError("Infobox not found.")

        # Initialize lists to store extracted data
        labels = []
        data = []

        # Iterate over each row of the table
        for row in infobox.find_all('tr'):
            # Exclude text inside reference class
            references = row.find_all(class_='reference')
            for reference in references:
                reference.extract()  # Remove reference text

            # Extract label and data
            label = row.find(class_='infobox-label')
            data_item = row.find(class_='infobox-data')
            
            if label and data_item:
                labels.append(label.get_text(strip=True))
                # Check if data item contains list items
                if data_item.find('ul'):
                    # Extract list items as a list
                    list_items = [li.get_text(strip=True).replace('\xa0', ' ') for li in data_item.find_all('li')]
                    data.append(list_items)
                else:
                    data.append(data_item.get_text(strip=True).replace('\xa0', ' '))

        return dict(zip(labels, data))