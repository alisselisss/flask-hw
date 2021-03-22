from flask import Flask, render_template, url_for
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user

from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()

    return render_template('works.html', title='works log', job_session=db_sess.query(Jobs),
                           user_session=db_sess.query(User), us=User,
                           css_file=url_for('static', filename='css/style.css'))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Password mismatch")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="This user already exists")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Register Form', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()