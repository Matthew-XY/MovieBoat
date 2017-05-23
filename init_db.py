#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random

from faker import Factory
import pymongo

from models import User, Movie
from models import db

fake = Factory.create('zh_CN')


def gen_user(amount=50):
    for i in range(amount):
        u = User(username=fake.name(), password='password')
        u.phone_number = fake.phone_number()
        u.avatar = 'http://opsfsk07z.bkt.clouddn.com/avatar-{}.jpg'.format(random.choice(range(50)))
        db.session.add(u)
        db.session.commit()


def get_mongo_cursor():
    client = pymongo.MongoClient('localhost')
    db = client['bt0_movie']

    cursor = db.bt0_movie.find()
    return cursor


def get_movie():
    i = 100
    for item in get_mongo_cursor():
        i += 1
        m = Movie(
            title=item['title'],
            cover=item['img'],
            info=item['info'],
            summary=item['summary'],
            brief_id=i,
        )

        db.session.add(m)
        db.session.commit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='你要初始化的表名')

    args = parser.parse_args()

    if args.name == 'user':
        gen_user()
    elif args.name == 'movie':
        get_movie()
