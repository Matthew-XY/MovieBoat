#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_moment import Moment


import configs

app = Flask(__name__)
app.config.from_object(configs)

babel = Babel(app)
moment = Moment(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
