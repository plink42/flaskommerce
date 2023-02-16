from flask import render_template, Blueprint
from flask.helpers import url_for
from flask_login import login_required
from store import db
from store.models import Products, Orders
from store.main.access import admin_required
from store.main.tools import Message

from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def home():
    today = datetime.now()
    recent = today - timedelta(days=7)
    total_prods = Products.query.count()
    total_orders = Orders.query.count()
    recent_orders = Orders.query.filter(Orders.orderdate>=int(recent.timestamp())).count()
    return render_template('admin/index.html', total_prods=total_prods, total_orders=total_orders, recent_orders=recent_orders)

@admin.route('/admin/catalog')
@login_required
def catalog():
    catalog = Products.query.all()
    return render_template('admin/products.html', catalog=catalog)