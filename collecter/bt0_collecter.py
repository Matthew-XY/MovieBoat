#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('localhost')
db = client['bt0_movie']


def collect_movies(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    L = soup.find_all('div', attrs={'class': 'masonry__item'})

    for x in L:
        uri = 'http://bt0.com' + x.a.get('href')
        img = x.img.get('src')
        title = x.img.get('alt')

        d = {
            'img': img,
            'uri': uri,
            'title': title,
            'info': get_movie_detail(uri)['info'],
            'summary': get_movie_detail(uri)['summary'],
        }
        print(d)
        db.bt0_movie.insert(d)


def get_movie_detail(uri):
    r = requests.get(uri)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    summary = soup.find_all('article')[0].text
    infos = soup.find_all('span', attrs={'class': 'tiny-title'})

    info = ''
    for i in infos:
        info += i.text + '\n'

    result = {
        'info': info,
        'summary': summary,
    }

    return result


if __name__ == '__main__':

    for i in range(0, 20):
        url = 'http://bt0.com/film-download/1-0-0-0-0-{}.html'.format(i)
        collect_movies(url)
