#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Require Auth for Admin
"""

from functools import wraps
from flask import flash, session, redirect, url_for

def require_auth_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None or session.get('user_role') != 1:
            flash('Only admin can view that page.', 'error-message')
            return redirect(url_for('auth.signin'))
        return func(*args, **kwargs)

    return decorated_function
