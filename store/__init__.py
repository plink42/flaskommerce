from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from currency_symbols import CurrencySymbols
from store.config import Config

import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.context_processor 
    def store_info():
        from store.models import StoreInfo
        storeinfo = StoreInfo.query.first()
        g.storename = storeinfo.storename
        g.storecurrency = storeinfo.currency
        g.storesymbol = CurrencySymbols.get_symbol(g.storecurrency)
        return dict(storename=storeinfo.storename,
                    storeurl=storeinfo.url,
                    storecurrency=storeinfo.currency,
                    categoryimages=os.path.join(app.config['IMAGE_DIR'], 'categories'),
                    productimages=os.path.join(app.config['IMAGE_DIR'], 'products'))
    
    @app.template_filter()
    def price(p):
        return f'{g.storesymbol}{p}'

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from store.users.routes import users
    from store.main.routes import main
    from store.admin.routes import admin
    from store.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    return app