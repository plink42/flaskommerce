from flask import current_app
from flask_login import UserMixin
from store import db, login_manager

import jwt

from datetime import timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class StoreInfo(db.Model):
    __table_name__ = 'storeinfo'
    id = db.Column(db.Enum('1'), primary_key=True)
    storename = db.Column(db.String(200))
    url = db.Column(db.String(100))

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(14), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    longdescription = db.Column(db.Text, nullable=False)
    shortdescription = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(14), nullable=False)
    retailPrice = db.Column(db.String(14), nullable=False)
    weight = db.Column(db.String(14), nullable=False)
    thumb = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    image_other = db.Column(db.String(255), nullable=False)
    updateDate = db.Column(db.Integer)
    categories = db.Column(db.String(255), nullable=False)
    liveDate = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    isFeatured = db.Column(db.Integer)

    def __repr__(self):
        return '<Product %r>'%self.sku

class Variants(db.Model):
    __tablename__ = 'variants'
    id = db.Column(db.Integer, primary_key=True)
    variant = db.Column(db.String(255))

    def __repr__(self):
        return '<Variant %r>'%self.variant

class VariantValue(db.Model):
    __tablename__ = 'variant_value'
    id = db.Column(db.Integer, primary_key=True)
    variantid = db.Column(db.Integer, db.ForeignKey('variants.id'))
    value = db.Column(db.String(255))
    sku = db.Column(db.String(100))
    priceincrement = db.Column(db.String(14))
    

    def __repr__(self):
        return '<Variant Value %r>'%self.value

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('products.id'))
    variantvalueid = db.Column(db.Integer, db.ForeignKey('variant_value.id'))
    variant_value = db.relationship('VariantValue', foreign_keys='ProductVariant.variantvalueid')
    products = db.relationship('Products', foreign_keys='ProductVariant.productid')


class ProductOptions(db.Model):
    __tablename__ = 'productoptions'
    id = db.Column(db.Integer, primary_key=True)
    optionid = db.Column(db.Integer, db.ForeignKey('options.id'))
    productid = db.Column(db.Integer, db.ForeignKey('products.id'))
    optiongroupid = db.Column(db.Integer, db.ForeignKey('optiongroups.id'))
    optionpriceincrement = db.Column(db.String(14))

    def __repr__(self):
        return '<ProductOptions %r>'%self.id

class Options(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    optionname = db.Column(db.String(255))

    def __repr__(self):
        return '<Options %r>'%self.id
    
class OptionGroups(db.Model):
    __tablename__ = 'optiongroups'
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(255))

    def __repr__(self):
        return '<OptionGroups %r>'%self.id

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))

    def __repr__(self):
        return '<Cateogries %r>'%self.name

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    orderamount = db.Column(db.String(14))
    shipname = db.Column(db.String(255))
    shipaddress1 = db.Column(db.String(255))
    shipaddress2 = db.Column(db.String(255))
    shipcity = db.Column(db.String(255))
    shipstate = db.Column(db.String(255))
    shipzip = db.Column(db.String(10))
    shipcountry = db.Column(db.String(255))
    shipphone = db.Column(db.String(255))
    shipid = db.Column(db.Integer, db.ForeignKey('shipping.id'))
    tax = db.Column(db.String(14))
    email = db.Column(db.String(255))
    shipcost = db.Column(db.String(14))
    orderdate = db.Column(db.Integer)
    statusid = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    statusdate = db.Column(db.Integer)
    trackingnumber = db.Column(db.String(255))

    def __repr__(self):
        return '<Orders %r>'%self.id

class Statuses(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    emailtemplateid = db.Column(db.Integer)

    def __repr__(self):
        return '<Statuses %r>'%self.description

class OrderDetails(db.Model):
    __tablename__ = 'orderdetails'
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.id'))
    productid = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.String(14))
    qty = db.Column(db.Integer)

    def __repr__(self):
        return '<OrderDetails %r>'%self.id

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    billaddress1 = db.Column(db.String(255))
    billaddress2 = db.Column(db.String(255))
    billcity = db.Column(db.String(255))
    billstate = db.Column(db.String(255))
    billzip = db.Column(db.String(255))
    billcountry = db.Column(db.String(255))
    registrationdate = db.Column(db.Integer)
    ip = db.Column(db.String(255))
    role = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode(
            {
                "user_id": self.id
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    
    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )['user_id']
            print(user_id)
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<Users %r>'%self.id

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    sessid = db.Column(db.Integer)
    item = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer, default=1)
    cost = db.Column(db.String(14), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return '<Cart %r>'%self.sessid

class Shipping(db.Model):
    __tablename__ = 'shipping'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    costper = db.Column(db.String(14), nullable=False)
    maxqty = db.Column(db.Integer)
    additional = db.Column(db.String(14))
    isdefault = db.Column(db.Integer, default=0)
    region = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Shipping %r>'%self.name