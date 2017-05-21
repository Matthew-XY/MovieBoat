#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost')
db = client['movie']


def collect_movies(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    L = soup.find_all('li', attrs={'class': 'post box row fixed-hight'})

    for x in L:
        img = x.find('div', attrs={'class': 'thumbnail'}).img.get('src')
        uri = x.find('div', attrs={'class': 'thumbnail'}).a.get('href')
        title = x.find('div', attrs={'class': 'thumbnail'}).a.get('title')
        entry_text = x.find('div', attrs={'class': 'entry_post'}).p.text

        d = {
            'img': img,
            'uri': uri,
            'title': title,
            'entry_text': entry_text,
            'description': get_description(uri),
        }

        print(d)
        db.movie.insert(d)


def get_description(uri):
    r = requests.get(uri)
    soup = BeautifulSoup(r.text, 'lxml')

    result = soup.find_all('meta', property='og:description')[-1].get('content')
    return result


if __name__ == '__main__':
    for i in range(219, 225):
        url = 'http://www.dy100.me/page/{}'.format(i)
        collect_movies(url)
