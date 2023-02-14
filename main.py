import random
import string
import json
import datetime

from flask import render_template, session, request, url_for, redirect
from sqlalchemy.sql import func

from store import app
from store import db
from store import models

from sqlalchemy import desc

db.init_app(app)

@app.context_processor
def get_cart_count():
    """return total items in cart
    
    Returns:
        int -- count of all items in cart
    """

    cartitems = 0
    for i in models.Cart.query.filter(models.Cart.sessid == session['cartid']).all():
        cartitems += i.qty
    return dict(cartitems = cartitems)

@app.context_processor
def store_info():
    return dict(store_name=app.config['STORE_NAME'], 
        store_title=app.config['STORE_TITLE'],
        company_name=app.config['COMPANY_NAME'],
        site_url=app.config['STORE_URL'],
        twitter_url=app.config['TWITTER'],
        facebook_url=app.config['FACEBOOK'],
        instagram_url=app.config['INSTAGRAM'],
        home_url=app.config['HOME_PAGE'],
        domestic = app.config['DOMESTIC_COUNTRY'])

@app.route('/')
def index():
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    featured = models.Products.query.filter(models.Products.isFeatured == 1).all()
    feature2 = models.Products.query.filter(models.Products.categories.like('%,5%')).limit(3).all()
    c = []
    for i in models.Cart.query.filter(models.Cart.sessid == session['cartid']).with_entities(models.Cart.item).all():
        c.append(i.item)    
    return render_template('index.html', featured = featured, feature2 = feature2, incart=c)

@app.route('/item/<id>')
def item(id):
    product = models.Products.query.filter(models.Products.id == id).one()
    variantvals = models.ProductVariant.query.filter(models.ProductVariant.productid == id).join(models.VariantValue).join(models.Variants).add_columns(models.VariantValue.value, models.VariantValue.sku, models.VariantValue.priceincrement, models.Variants.variant).all()
    variants = models.ProductVariant.query.filter(models.ProductVariant.productid == id).join(models.VariantValue).join(models.Variants).with_entities(models.Variants.variant).distinct()
    variants = [item[0] for item in variants]
    return render_template('item.html', product=product, variantvals = variantvals, variants=variants)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/store', defaults={'key': None, 'val': None})
@app.route('/store/<key>/<val>')
def store(key, val):
    if key:
        if key == 'cat':
            top = models.Categories.query.filter(models.Categories.id == val).one() 
            prods = models.Products.query.order_by(desc(models.Products.updateDate)).filter(models.Products.categories.like('%{}%'.format(val))).all()
        elif key == 'price':
            if val == '10to30':
                top = {'name': '$10 to $30', 'description': 'Products between $10 and $30 USD'}
                prods = models.Products.query.filter(models.Products.price >= 10).filter(models.Products.price <= 30).all()
            elif val == '30to50':
                top = {'name': '$30 to $50', 'description': 'Products between $30 and $50 USD'}
                prods = models.Products.query.filter(models.Products.price >= 30).filter(models.Products.price <= 50).all()
            elif val == '50to100':
                top = {'name': '$50 to $100', 'description': 'Products between $50 and $100 USD'}
                prods = models.Products.query.filter(models.Products.price >= 50).filter(models.Products.price <= 100).all()
            elif val == 'over100':
                top = {'name': 'Over $100', 'description': 'Products over $100 USD'}
                prods = models.Products.query.filter(models.Products.price >= 100).all()
            else: 
                top = {'name': 'store', 'description': 'the best store on the planet. find and buy everything.'}
                prods = models.Products.query.order_by(desc(models.Products.updateDate)).all()
        else:
            top = {'name': 'store', 'description': 'the best store on the planet. find and buy everything.'}
            prods = models.Products.query.order_by(desc(models.Products.updateDate)).all()
    else:
        top = {'name': 'store', 'description': 'the best store on the planet. find and buy everything.'}
        prods = models.Products.query.order_by(desc(models.Products.updateDate)).all()
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess

    filters = [
            {'key': 'price',
            'val': '10to30',
            'display': '$10 to $30'},
            {'key': 'price',
            'val': '30to50',
            'display': '$30 to $50'},
            {'key': 'price',
            'val': '50to100',
            'display': '$50 to $100'},
            {'key': 'price',
            'val': 'over100',
            'display': 'Over $100'}
        ]
    cats = models.Categories.query.order_by(models.Categories.name).all()
    c = []
    for i in models.Cart.query.filter(models.Cart.sessid == session['cartid']).with_entities(models.Cart.item).all():
        c.append(i.item)    
    return render_template('store_2.html', prods = prods, cats = cats, incart= c, top = top, filters=filters)

@app.route('/categories/<catid>')
def categories(catid):
    if catid:
        prods = models.Products.query.order_by(models.Products.updateDate).filter(models.Products.categories.like('%{}%'.format(catid))).all()
        cat = models.Categories.query.filter(models.Categories.id == catid).one()
        c = []
        for i in models.Cart.query.filter(models.Cart.sessid == session['cartid']).with_entities(models.Cart.item).all():
            c.append(i.item)    
        return render_template('categories.html', prods = prods, cat = cat, incart=c)
    else:
        return redirect(url_for('error'))

@app.route('/add_to_cart', defaults={'sku': None, 'cost': None}, methods=['GET', 'POST'])
@app.route('/add_to_cart/<sku>/<cost>')
def add_to_cart(sku, cost):
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    if request.method == 'GET':
        if sku:
            incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
            if incart:
                models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).update({models.Cart.qty: models.Cart.qty +1})
                db.session.commit()
            else:
                itemadd = models.Cart(sessid=session['cartid'], item=sku, qty=1, cost=cost, date=datetime.datetime.now())
                db.session.add(itemadd)
                db.session.commit()
        return redirect(url_for('show_cart'))
    elif request.method == 'POST':
        variants = []
        for f in request.form:
            if f == 'sku':
                sku = request.form.get(f)
            if f == 'price':
                cost = request.form.get(f)
            if f == 'qty':
                qty = request.form.get(f)
            if f.startswith('product-variant'):
                variants.append(request.form.get(f))
        if sku:
            fullsku = sku
            for v in variants:
                fullsku += '-{}'.format(v)
        if fullsku:
            incart = models.Cart.query.filter(models.Cart.item == fullsku).filter(models.Cart.sessid == session['cartid']).all()
            if incart:
                models.Cart.query.filter(models.Cart.item == fullsku).filter(models.Cart.sessid == session['cartid']).update({models.Cart.qty: models.Cart.qty + int(qty)})
                db.session.commit()
            else:
                itemadd = models.Cart(sessid=session['cartid'], item=fullsku, qty=int(qty), cost=cost, date=datetime.datetime.now())
                db.session.add(itemadd)
                db.session.commit()
        return redirect(url_for('show_cart'))

@app.route('/delete_from_cart/<sku>')
def delete_from_cart(sku):
    if sku:
        incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
        if incart:
            models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).delete()
            db.session.commit()
    return redirect(url_for('show_cart'))

@app.route('/update_cart/<sku>')
def update_cart(sku):
    qty = request.args.get('qty')

    if int(qty) <= 0:
        qty = 0
    if qty and qty != 0:
        print('qty > 0')
        if sku:
            incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
            if incart:
                models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).update({models.Cart.qty: int(qty)})
                db.session.commit()
    else:
        print('qty == 0')
        if sku:
            incart = models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).all()
            if incart:
                models.Cart.query.filter(models.Cart.item == sku).filter(models.Cart.sessid == session['cartid']).delete()
                db.session.commit()
    return redirect(url_for('show_cart'))
    
@app.route('/cart')
def show_cart():
    if 'cartid' not in session:
        randomsess = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        session['cartid'] = randomsess
    thecart = models.Cart.query.filter(models.Cart.sessid == session['cartid']).all()
    cartdisp = []

    cart_total = 0
    for cart in thecart:
        item = cart.item.split('-')
        thesku = item[0]
        del item[0]
        variants = []
        for v in item:
            vname = models.VariantValue.query.filter(models.VariantValue.sku == v).one()
            print(vname.value)
            variants.append(vname.value)
        prod = models.Products.query.filter(models.Products.sku == thesku).limit(1).all()
        total = cart.cost*cart.qty
        data = {'sku': cart.item, 'cost': cart.cost, 'qty': cart.qty, 'name': prod[0].name, 'image': prod[0].image, 'thumb': prod[0].thumb, 'total': '{:0.2f}'.format(total), 'variants': variants}
        cart_total += total
        cartdisp.append(data)
    return render_template('cart.html', thecart = cartdisp, cart_total = '{:0.2f}'.format(cart_total))

@app.route('/checkout')
def checkout_1():
    return render_template('checkout_1.html')

@app.route('/checkout/info')
def checkout_2():
    thecart = models.Cart.query.filter(models.Cart.sessid == session['cartid']).all()
    cart_total = 0
    for cart in thecart:
        total = cart.cost*cart.qty
        cart_total += total
    return render_template('checkout_2.html', cart_total='{:0.2f}'.format(cart_total))

@app.route('/checkout/shipping', methods=["GET", "POST"])
def checkout_3():
    if request.method == "GET":
        return redirect(url_for('show_cart'))
    if request.form['shipcountry'] == app.config['DOMESTIC_COUNTRY']:
        filt = 'domestic'
    else:
        filt = 'international'
    shipping = models.Shipping.query.filter(models.Shipping.region == filt).all()
    cartitems = get_cart_count()['cartitems']
    ship_options = []
    for s in shipping:
        if cartitems < s.maxqty:
            opt = {'id': s.id, 'name': s.name, 'description': s.description, 'total_cost': '{:0.2f}'.format(s.costper), 'isdefault': s.isdefault}
            ship_options.append(opt)
        else:
            cost = float(s.costper + (cartitems - s.maxqty) * s.additional)
            cost = '{:0.2f}'.format(cost)
            opt = {'id': s.id, 'name': s.name, 'description': s.description, 'total_cost': cost, 'isdefault': s.isdefault}
            ship_options.append(opt)
    print(ship_options)

    if request.method == "POST":
        return render_template('checkout_3.html', person=request.form, ship_options=ship_options)
    

@app.route('/getstates/<country>')
def get_states(country):
    with open('app/static/json/provinces.json', encoding='utf-8') as f:
        data = json.load(f)
    output = {}
    for i in data:
        if i['country'].upper() == country.upper():
            try:
                short = i['short']
            except:
                short = False
            if not short:
                output[i['name']] = i['name']
            else:
                output[short] = i['name']
    return json.dumps(output, indent=4)

@app.route('/error/<error>')
def error(error):
    return "There was and ERROR: {}".format(error)