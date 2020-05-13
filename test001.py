import mysql.connector
import requests
from bs4 import BeautifulSoup

class parser:

    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'accept': '*/*'}




    # def __init__(self, url): #table
    #     self.URL = url
    #     self.URL = url
    #     # self.table = table_name

    def table(self):
        pass

    def get_html(self, params=None):
        r = requests.get(self.URL, headers=self.HEADERS, params=params)
        return r

    def get_content(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_pages_count(self, html):
        pass


    # def _save_sql(self, items):
    #     self.db = mysql.connector.connect(host='localhost', user='root', password='1234', database='films')
    #     self.cursor = self.db.cursor()
    #     self.cursor.execute('CREATE TABLE {self.table} (ID int PRIMARY KEY AUTO_INCREMENT, title VARCHAR(70), description VARCHAR(250), producer VARCHAR(70), link VARCHAR(100)')
    #
    #     for i in items:
    #         sqlFormula = 'INSERT INTO afisha (title, description, link, producer) VALUES(%s, %s, %s, %s)'
    #         films = (([i['title'],i['desc'], i['producer'], 'link']))
    #         self.cursor.execute(sqlFormula, films)
    #     self.db.commit()

    def parse(self):
        html = self.get_html(self.URL)
        if html.status_code == 200:
            self.films = []
            self.pages_count = self.get_pages_count(html.text)
            for page in range(1,self.pages_count+1):
                html = self.get_html(self.URL)
                self.films.extend(self.get_content(html.text))
            # self._save_sql(self.films)
            print(self.films)
            print(len(self.films))
            print(f'RECIVED {len(self.films)}')
        else:
            print('ERROR')


class kinoAfisha(parser):

    URL = 'https://www.kinoafisha.info/rating/movies/'

    kinoAfisha_host = 'https://www.kinoafisha.info'

    table_name = 'afisha'


    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='films_right')

        self.films = []
        for item in items:
            self.films.append({
                'title': item.find('a', class_='films_name').get_text(),
                'desc': '' + item.find('a', class_='films_name').get('href'),
                'producer': item.find_all('span', class_='films_info')[-1].get_text().lstrip('\n').replace(' ', ''),
                'link': self.kinoAfisha_host + item.find('a', class_='films_name').get('href'),

            })
        return self.films

    def get_pages_count(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.pagination = self.soup.find_all('a', class_='pager_item')
        if self.pagination:
            return int(self.pagination[-1].get_text())
        else:
            return 1

kinoAfishaa = kinoAfisha()
kinoAfishaa.parse()