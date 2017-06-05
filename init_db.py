#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random

import datetime

import math
from faker import Factory
import pymongo

from models import User, Movie, Comment, ChargeRecord, CustomRecord, MoviePrice
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
    i = 1000
    for item in get_mongo_cursor():
        i += 1
        m = Movie(
            title=item['title'],
            cover=item['img'],
            info=item['info'],
            summary=item['summary'].lstrip(),
            brief_id=i,
            video_uri='http://oh6k349gl.bkt.clouddn.com/sample-001.mp4'
        )

        mp = MoviePrice(
            movie=m,
            price=math.floor(random.random() * 20)
        )

        db.session.add(m)
        db.session.add(mp)
        db.session.commit()


def gen_comment(amount=100):
    comments = [
        '太好看了！而且非常难得的是，电影并没有在经历DCEU几番口碑失败后向Y靠拢，反而是在扎克施耐德打下的原有主题基调下做的更好更成熟',
        '大家快跑啊骗钱的又来了',
        '本来以为正片就够尴尬了，没想到五个彩蛋更是尴尬到顶点',
        '太空电影可以不拍成一个人孤独战斗的缩影。无论多么绝望都剩下最后一点掐不灭的希望，这点太喜欢了，这种设定也很适合马特达蒙自身',
        'M工作室目前最棒的电影，没有之一，必看！比Y系列更上一个档次！ ',
        '过于浓重的说教意味，毫无逻辑的人物设定',
        '很棒，有史诗的感觉，画面感各方面都不错，特效也不错',
        '看完了，没有说的那么好看，情节上好多都比较牵强',
    ]

    for i in range(amount):
        u = random.choice(User.query.all())
        m = random.choice(Movie.query.all())
        c = Comment(
            user=u,
            movie=m,
            comment_time=datetime.datetime.now() + datetime.timedelta(fake.random_digit()),
            content=random.choice(comments),
            point=random.choice(range(5)) + 1,
        )
        db.session.add(c)
        db.session.commit()


def gen_charge_record(amount=100):
    for i in range(amount):
        u = random.choice(User.query.all())
        money = math.floor(random.random() * 20)
        cr = ChargeRecord(
            user=u,
            charge_time=datetime.datetime.now() + datetime.timedelta(fake.random_digit()),
            money=money,
        )
        u.balance += money
        db.session.add(cr)
        db.session.add(u)
        db.session.commit()


def gen_custom_record(amount=100):
    for i in range(amount):
        u = random.choice(User.query.all())
        m = random.choice(Movie.query.all())
        money = MoviePrice.query.get(m.id).price

        if u.balance > money:
            cr = CustomRecord(
                customer=u,
                movie=m,
                custom_time=datetime.datetime.now() + datetime.timedelta(fake.random_digit()),
                money=money,
            )
            u.balance -= money
            db.session.add(cr)
            db.session.add(u)
            db.session.commit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='你要初始化的表名')

    args = parser.parse_args()

    if args.name == 'user':
        gen_user()
    elif args.name == 'movie':
        get_movie()
    elif args.name == 'comment':
        gen_comment()
    elif args.name == 'charge':
        gen_charge_record()
    elif args.name == 'custom':
        gen_custom_record()
