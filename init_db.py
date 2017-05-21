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
    db = client['movie']

    cursor = db.movie.find()
    return cursor


def get_movie():
    for item in get_mongo_cursor():
        m = Movie(
            title=item['title'],
            cover=item['img'],
            staffs=item['entry_text'],
            description=item['description'],
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
