from datetime import datetime, date

from flask import render_template, redirect, url_for, session, Blueprint
from flask_login import current_user, login_required

from todolist import db

main = Blueprint('main', __name__)


@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect(url_for('users.login'))