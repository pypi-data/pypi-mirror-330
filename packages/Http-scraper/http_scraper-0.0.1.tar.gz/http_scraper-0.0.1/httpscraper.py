import pandas as pd
import requests
from bs4 import BeautifulSoup


class RecipeScraper:
    def __init__(self) -> None:
        self.soup = None
        self.data_frame = None

    def ScrapeUrl(self, url: str):
        response = requests.get(url)
        response.endcoding = 'utf-8'
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def get_tables_data(self) -> pd.DataFrame:
        tables = self.soup.find_all('table')[1:]
        headers = self.soup.find_all('h2')
        data_table = []
        for i, table in enumerate(tables):
            table_rows = table.find_all('tr')[1:]
            data_table.append({'table_name': headers[i].text,
                               "table_data": []
                               })
            for row in table_rows:
                cells = row.find_all('td')
                data_table[i]['table_data'].append({
                    'name': cells[0].text,
                    'ingredients': cells[1].text,
                    'image': cells[2].find('img')['src'],
                    'desc': cells[3].text
                })
            self.data_frame = pd.DataFrame(data_table)
            return self.data_frame



