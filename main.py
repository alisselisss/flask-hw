from flask import Flask, render_template, url_for
from werkzeug.utils import redirect

from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.RegisterForm import RegisterForm

app = Flask(__name__)
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
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
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


@app.route('/login')
def login():
    return render_template('base.html', title='')


def main():
    db_session.global_init("db/blogs.db")
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()