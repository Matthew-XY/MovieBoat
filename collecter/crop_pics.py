#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import requests
import shutil
from PIL import Image

from models import db, Movie


def download_movie_covers():
    for movie in Movie.query.all():
        r = requests.get(movie.cover, stream=True)
        with open('pics/movie-{}.jpg'.format(movie.brief_id), 'wb') as f:
            print(movie.title)
            shutil.copyfileobj(r.raw, f)


def crop_pics():
    for pic in os.listdir('pics'):
        img = Image.open(os.path.join('pics', pic))
        img2 = img.crop((0, 0, 300, 444))
        img2.save(os.path.join('pics_croped', pic))


def change_cover_url():
    for movie in Movie.query.all():
        movie.cover = 'http://opsfsk07z.bkt.clouddn.com/movie-{}.jpg'.format(movie.brief_id)
        db.session.add(movie)
        db.session.commit()


if __name__ == '__main__':
    download_movie_covers()
    crop_pics()
    change_cover_url()
