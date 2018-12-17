#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Smallest possible cgi-script to execute a WSGI application like Flask.
"""

from app import app
app.run(host='0.0.0.0', port=8080, debug=True)
