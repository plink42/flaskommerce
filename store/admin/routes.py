from flask import render_template, Blueprint, request, flash, current_app, redirect
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from currency_symbols import currency_symbols
from currency_symbols._constants import CURRENCY_SYMBOLS_MAP

from store import db
from store.models import Products, Orders, Categories, ProductCategory, StoreInfo
from store.main.access import admin_required
from store.main.tools import Message
from store.admin.forms import StoreInfoForm, ProductForm, CategoryForm, DeleteConfirm

from datetime import datetime, timedelta
import os
 
admin = Blueprint('admin', __name__)

def upload_image(image, dir):
    if image.data:
        imagename = image.data.filename
        dir = os.path.join(current_app.root_path, current_app.config['IMAGE_DIR'], dir)
        file = os.path.join(dir, secure_filename(imagename))
        image.data.save(file)
    else:
        imagename = None
    return imagename

@admin.route('/admin')
@login_required
@admin_required
def home():
    today = datetime.now()
    recent = today - timedelta(days=7)
    total_prods = Products.query.count()
    total_orders = Orders.query.count()
    recent_orders = Orders.query.filter(Orders.orderdate>=int(recent.timestamp())).count()
    return render_template('admin/index.html', total_prods=total_prods, total_orders=total_orders, recent_orders=recent_orders)

@admin.route('/admin/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    info = StoreInfo.query.first()
    form = StoreInfoForm()
    currencies = []
    for s in CURRENCY_SYMBOLS_MAP:
        currencies.append((s, s))
    form.currency.choices = currencies
    if form.validate_on_submit():
        info.storename = form.data['storename']
        info.url = form.data['url']
        info.currency = form.data['currency']
        info.address1 = form.data['address1']
        info.address2 = form.data['address2']
        info.city = form.data['city']
        info.stateprovince = form.data['stateprovince']
        info.postalcode = form.data['postalcode']
        info.country = form.data['country']
        db.session.commit()
        flash('Store Settings Saved', 'success')        
    form.currency.default = info.currency
    form.country.default = info.country
    form.process()
    return render_template('admin/settings.html', form=form, info=info)
    
@admin.route('/admin/catalog')
@login_required
@admin_required
def catalog():
    catalog = Products.query.all()
    return render_template('admin/products.html', catalog=catalog)

@admin.route('/admin/catalog/products')
@login_required
@admin_required
def products():
    category_id = request.args.get('category_id')
    if category_id:
        products = Products.query.join(ProductCategory, Products.id==ProductCategory.productid).filter(ProductCategory.categoryid==category_id).all()
    else:
        products = Products.query.all()
    return render_template('admin/products.html', products=products)

@admin.route('/admin/catalog/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    categories = Categories.query.all()
    choices = []
    for c in categories:
        choices.append((c.id, c.name))
    form.categories.choices = choices
    if form.validate_on_submit():
        thumbname = upload_image(form.thumb, 'products')
        imagename = upload_image(form.image, 'products')
        livedate = int(datetime.combine(form.livedate.data, datetime.min.time()).timestamp())
        prod = Products(
            sku=form.sku.data,
            name=form.name.data,
            longdescription=form.longdescription.data,
            shortdescription=form.shortdescription.data,
            price=form.price.data,
            retail=form.retail.data,
            weight=form.weight.data,
            thumb=thumbname,
            image=imagename,
            imageother='',
            livedate=livedate,
            stock=form.stock.data,
            isfeatured=form.isfeatured.data
        )
        db.session.add(prod)
        db.session.commit()
        print(prod.id)
        for cat in form.categories.data:
            c = ProductCategory(
                productid=prod.id,
                categoryid=cat
            )
            db.session.add(c)
            db.session.commit()
        flash(f'Successfully added {prod.name}', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/add_product.html', form=form)

@admin.route('/admin/catalog/products/edit/<productid>')
@login_required
@admin_required
def edit_product(productid):
    return productid

@admin.route('/admin/catalog/products/delete/<productid>')
@login_required
@admin_required
def delete_product(productid):
    return productid

@admin.route('/admin/catalog/categories')
@login_required
@admin_required
def categories():
    categories = Categories.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin.route('/admin/catalog/categories/edit/<categoryid>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(categoryid):
    form = CategoryForm()
    category = Categories.query.filter(Categories.id==categoryid).first()
    if form.validate_on_submit():
        if form.image.data:
            imagename = form.image.data.filename
            dir = os.path.join(current_app.root_path, current_app.config['IMAGE_DIR'], 'categories')
            file = os.path.join(dir, secure_filename(imagename))
            form.image.data.save(file)
        else:
            imagename = None
        category.name = form.name.data
        category.description = form.description.data
        category.image = imagename
        db.session.commit()
        flash(f'{category.name} updated successfully.', 'success')
        return redirect(url_for('admin.categories'))
    form.description.data=category.description
    return render_template('admin/edit_category.html', form=form, category=category)

@admin.route('/admin/catalog/categories/delete/<categoryid>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_category(categoryid):
    form = DeleteConfirm()
    if form.validate_on_submit():
        if form.deleteid.data == categoryid:
            d = Categories.query.filter(Categories.id==form.deleteid.data).delete()
            if d:
                db.session.commit()
                flash(f'Successfully deleted: {form.deletename.data}', 'success')
                return redirect(url_for('admin.categories'))
            else:
                flash(f'A error occured while deleting: {form.deletename.data}', 'error')
                return redirect(url_for('admin.categories'))
    category = Categories.query.filter(Categories.id==categoryid).first()
    form.deleteid.data = category.id
    form.deletename.data = category.name
    return render_template('admin/delete_category.html', form=form, category=category)

@admin.route('/admin/catalog/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if form.image.data:
            imagename = form.image.data.filename
            dir = os.path.join(current_app.root_path, current_app.config['IMAGE_DIR'], 'categories')
            file = os.path.join(dir, secure_filename(imagename))
            form.image.data.save(file)
        else:
            imagename = None
        category = Categories(
            name = form.name.data,
            description = form.description.data,
            image = imagename
        )
        db.session.add(category)
        db.session.commit()
        flash(f'{category.name} added successfully.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/add_category.html', form=form)