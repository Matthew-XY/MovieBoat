#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from uuid import uuid1

from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

from flask_login import UserMixin

from flask_app import app

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(512), nullable=False)

    balance = db.Column(db.Float, default=0.0)
    avatar = db.Column(db.String(1024), nullable=True)
    phone_number = db.Column(db.String(16), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = uuid1().hex

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def validate_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Movie(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    brief_id = db.Column(db.Integer, unique=True)
    cover = db.Column(db.String(1024), nullable=False)
    info = db.Column(db.String(128), nullable=False)
    summary = db.Column(db.String(1024), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = uuid1().hex

    def __repr__(self):
        return '<Movie {}>'.format(self.title)


class CustomRecord(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    custom_time = db.Column(db.DateTime, nullable=False, doc='消费时间')

    customer_id = db.Column(db.String(32), db.ForeignKey('user.id', ondelete='cascade'), doc='消费的消费者id')
    customer = db.relationship('User', backref=db.backref('custom_records', lazy='dynamic'))

    movie_id = db.Column(db.String(32), db.ForeignKey('movie.id', ondelete='cascade'))
    movie = db.relationship('Movie', backref=db.backref('custom_records', lazy='dynamic'))

    money = db.Column(db.Float, nullable=False, default=0.0, doc='消费金额')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = uuid1().hex
        self.custom_time = datetime.now()

    def __repr__(self):
        return '<CustomRecord {}>'.format(self.id)


class ChargeRecord(db.Model):
    id = db.Column(db.String(32), primary_key=True, doc='id主键')
    charge_time = db.Column(db.DateTime, nullable=False, doc='充值时间')
    money = db.Column(db.Float, nullable=False, default=0.0, doc='充值金额')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = uuid1().hex
        self.charge_time = datetime.now()

    def __repr__(self):
        return '<ChargeRecord {}>'.format(self.id)
