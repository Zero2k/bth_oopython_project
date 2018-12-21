#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Test Restaurant Module
"""

import unittest

from app import db
from app.modules.restaurant.models import Restaurant, Table, Booking

class TestRestaurantModule(unittest.TestCase):
    """ Test restaurant module and methods """

    def test_create_restaurant(self):
        """ Create Restaurant """
        restaurant = Restaurant.create(name="restaurant Create", \
            address="address 1", food="seafood", user_id=1)
        self.assertEqual(restaurant.name, "restaurant Create")
        self.assertEqual(restaurant.address, "address 1")
        self.assertEqual(restaurant.user_id, 1)

        Restaurant.delete(restaurant)

    def test_create_table(self):
        """ Create Table """
        restaurant = Restaurant.create(name="restaurant Table", \
            user_id=1)
        table = Table.create(name="table 1", capacity=4, minimum=2, \
            restaurant_id=restaurant.id)
        self.assertEqual(table.restaurant_id, restaurant.id)

    def test_create_booking(self):
        """ Create Booking """
        table = Table.query.order_by('-id').first()
        new_booking = Booking.create(email="test@test.com", \
            user_id=1, table_id=table.id)
        self.assertEqual(new_booking.table_id, table.id)

        Booking.delete(new_booking)

    def test_delete_restaurant(self):
        """ Delete Restaurant """
        last_restaurant = Restaurant.query.order_by('-id').first()
        self.assertEqual(last_restaurant.name, "restaurant Table")
        Restaurant.delete(last_restaurant)
