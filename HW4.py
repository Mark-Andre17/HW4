import json
import requests
from bs4 import BeautifulSoup
from hashlib import md5

url_wiki = 'https://en.wikipedia.org'
url = 'https://en.wikipedia.org/wiki/List_of_country-name_etymologies'
file_json = 'countries.json'


def save_file(filename, countries_dict):
    json_file = json.dumps(countries_dict, indent=2)
    with open(filename, 'w') as f:
        f.write(json_file)


def json_read_hash(filename):
    with open(filename, encoding='utf8') as file:
        for line in file:
            yield md5(bytearray(line, encoding='utf8'))


class Wiki:
    def __init__(self, filename):
        with open(filename, encoding='utf-8') as file:
            json_countries = json.load(file)
            self.countries = [country["name"]["common"].replace(' ', '_') for country in json_countries]

    def __iter__(self):
        return self

    def __next__(self):
        if self.countries:
            req = requests.get(url)
            html = req.text
            req.raise_for_status()
            soup = BeautifulSoup(html, 'html.parser')
            countries_dict = {}
            for country in self.countries:
                links = soup.find_all('span', class_='mw-headline', id=country)
                for link in links:
                    href_contries = url_wiki + link.a.get('href')
                    countries_dict[country] = [href_contries]
            return countries_dict
        else:
            raise StopIteration


if __name__ == '__main__':
    for a in Wiki('countries.json'):
        save_file('w.json', a)
    for hash in json_read_hash('w.json'):
        print(hash)
