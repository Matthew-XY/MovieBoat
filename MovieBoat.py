from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db
from models import Movie, User
from flask_app import app

from init_db import gen_user, get_movie


# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
# manager.run()


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')

    user = User.query.filter_by(phone_number=phone).first()

    if not user:
        flash('用户不存在')
        return redirect(url_for('.index'))

    if user.validate_password(password):
        return redirect(url_for('.index'))


if __name__ == '__main__':
    init_login()
    app.run(debug=True)
