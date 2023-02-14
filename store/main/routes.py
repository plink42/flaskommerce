from flask import render_template, Blueprint, session, current_app
from flask_login import login_required
from flask.helpers import url_for
from store.models import Products

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    return render_template('test.html')