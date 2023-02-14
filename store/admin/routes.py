from flask import render_template, Blueprint
from flask.helpers import url_for
from flask_login import login_required
from store import db
from store.models import Products
from store.main.access import admin_required
from store.main.tools import Message

from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
@admin_required
def home():
    return render_template('test.html')