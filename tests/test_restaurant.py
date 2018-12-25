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

    def test_edit_restaurant(self):
        """ Update Restaurant """
        current_restaurant = Restaurant.query.order_by('-id').first()

        current_restaurant.name = "restaurant Edit"
        current_restaurant.address = "address 2"

        Restaurant.update(current_restaurant)

        updated_restaurant = Restaurant.query.order_by('-id').first()
        self.assertEqual(updated_restaurant.name, "restaurant Edit")
        self.assertEqual(updated_restaurant.address, "address 2")

        Restaurant.delete(updated_restaurant)

    def test_create_table(self):
        """ Create Table """
        restaurant = Restaurant.create(name="restaurant Table", \
            user_id=1)
        table = Table.create(name="table 1", capacity=4, minimum=2, \
            restaurant_id=restaurant.id)
        self.assertEqual(table.restaurant_id, restaurant.id)

    def test_edit_table(self):
        """ Update Table """
        current_table = Table.query.order_by('-id').first()

        current_table.name = "table test"
        current_table.capacity = 3
        current_table.minimum = 3

        Table.update(current_table)

        updated_table = Table.query.order_by('-id').first()
        self.assertEqual(updated_table.name, "table test")
        self.assertEqual(updated_table.capacity, 3)
        self.assertEqual(updated_table.minimum, 3)

        Table.delete(updated_table)

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
