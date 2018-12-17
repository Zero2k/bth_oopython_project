#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Smallest possible cgi-script to execute a WSGI application like Flask.
"""

try:
    from wsgiref.handlers import CGIHandler
    from app import app

    CGIHandler().run(app)

except Exception as e:
    import traceback

    print("Content-Type: text/plain;charset=utf-8")
    print("")
    print(traceback.format_exc())
