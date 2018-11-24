#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Booking
"""

# Importera relevanta moduler
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def main():
    """ Home route """
    return render_template("home.html", title="Welcome to Booking.com")


@app.route("/login")
def login():
    """ Login route """
    return render_template("login.html", title="Welcome to Booking.com")

@app.route("/sign-up")
def signup():
    """ Register route """
    return render_template("signup.html", title="Welcome to Booking.com")


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    import traceback
    return "<p>Flask 500<pre>" + traceback.format_exc()


if __name__ == "__main__":
    app.run(debug=True)
