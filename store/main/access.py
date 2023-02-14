from functools import wraps
from flask import request, flash, redirect
from flask.helpers import url_for
from flask_login import current_user

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        area = request.blueprint
        if area == 'admin':
            if current_user.role == 1:
                return func(*args, **kwargs)
            else:
                flash(f'You do not have access to {area}. Your attempt has been logged.', 'danger')
                return redirect(url_for('errors.not_allowed'))
        else:
            flash(f'You do not have access to {area}. Your attempt has been logged.', 'danger')
            return redirect(url_for('errors.not_allowed'))