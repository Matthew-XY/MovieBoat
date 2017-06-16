#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_babelex import Babel

app = Flask(__name__)
babel=Babel(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.secret_key = 'MovieBoat'
