from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
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




def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies, user=current_user)


@app.route('/logout')
@login_required
def logout():
    user = User.query.get(session.get('user_id'))
    logout_user()
    return redirect(url_for('.index'))


@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')

    user = User.query.filter_by(phone_number=phone).first()

    ret = {}

    if not user:
        ret['code'] = 1
        ret['message'] = '用户不存在'
        return jsonify(ret)

    if user.validate_password(password):
        ret['code'] = 0
        login_user(user)
    else:
        ret['code'] = 2
        ret['message'] = '密码错误'

    return jsonify(ret)


if __name__ == '__main__':
    init_login()
    app.run(debug=True)
