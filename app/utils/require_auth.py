from flask import flash, session, redirect, url_for
from functools import wraps

def require_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            flash('You need to login in order view that page.', 'error-message')
            return redirect(url_for('auth.signin'))
        return func(*args, **kwargs)

    return decorated_function
