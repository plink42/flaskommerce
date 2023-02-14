from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from store import db, bcrypt
from store.main.tools import Message
from store.models import User
from store.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from store.users.utils import save_picture, send_reset_email, verify_register_token, email_on_register

from datetime import datetime

users = Blueprint('users', __name__)


@users.route("/reg/<token>", methods=['GET', 'POST'])
def register_special(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    signature = verify_register_token(token)
    mess = Message()
    if signature['error']:
        email = 0
        flash(mess.error('The link has expired! Request a new link.'), 'danger')
        return redirect(url_for('main.home'))
    else:
        email = signature['email']
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, role=2, password=hashed_password, active=1)
        db.session.add(user)
        db.session.commit()
        admins = User.query.filter(User.role==1).all()
        admin_emails = []
        for a in admins:
            admin_emails.append(a.email)
        email_on_register(admin_emails, user.email)
        flash(mess.success('Your account has been created! You are now able to log in'), 'danger')
        return redirect(url_for('users.login'))
    else:
        print(form.errors)
    return render_template('/users/register.html', title='Register', form=form, email=email)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    mess = Message()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.fname.data, lastname=form.lname.data, email=form.email.data, role=2, password=hashed_password, active=False)
        db.session.add(user)
        db.session.commit()
        flash(mess.success('Your account has been created! You are now able to log in'), 'danger')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    mess = Message()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.active:
            login_user(user, remember=form.remember.data)
            user.lastlog = datetime.now()
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(mess.error('Login Unsuccessful. Please check email and password'), 'danger')
    return render_template('/users/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    mess = Message()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        current_user.fname = form.fname.data
        current_user.lname = form.lname.data
        db.session.commit()
        flash(mess.success('Your account has been updated!'), 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.lname.data = current_user.lname
        form.fname.data = current_user.fname
    else:
        print(form.errors)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('/users/account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    mess = Message()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(mess.info('An email has been sent with instructions to reset your password.'), 'info')
        return redirect(url_for('users.login'))
    return render_template('/users/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    mess = Message()
    if user is None:
        flash(mess.error('That is an invalid or expired token'), 'danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(mess.success('Your password has been updated! You are now able to log in'), 'success')
        return redirect(url_for('users.login'))
    return render_template('/users/reset_token.html', title='Reset Password', form=form)
