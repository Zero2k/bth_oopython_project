#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Exception handler
"""

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class EmailExists(Error):
    """Raised when email already exists"""
    pass

class DeleteUser(Error):
    """Raised when a user can't be deleted """
    pass


# Table Class
class AddTable(Error):
    """Raised when a table can't be created """
    pass

class EditTable(Error):
    """Raised when a table can't be changed """
    pass

class DeleteTable(Error):
    """Raised when a booking can't be deleted """
    pass


# Booking Class
class DeleteBooking(Error):
    """Raised when a booking can't be deleted """
    pass


# Restaurant Class
class AddRestaurant(Error):
    """Raised when a restaurant can't be created """
    pass

class ShowRestaurant(Error):
    """Raised when a restaurant can't be found """
    pass

class EditRestaurant(Error):
    """Raised when a restaurant can't be changed """
    pass

class SearchRestaurant(Error):
    """Raised when a restaurant can't be found """
    pass

class DeleteRestaurant(Error):
    """Raised when a restaurant can't be deleted """
    pass
