from flask import Flask, render_template, url_for

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def main():
    db_session.global_init('db/blogs.db')

    db_sess = db_session.create_session()

    return render_template('works.html', title='works log', job_session=db_sess.query(Jobs),
                           user_session=db_sess.query(User), us=User,
                           css_file=url_for('static', filename='css/style.css') + "?q=1280549780")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)