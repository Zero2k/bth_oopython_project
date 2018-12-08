import unittest

from app import db
from app.modules.restaurant.models import Restaurant, Table

class TestRestaurantModule(unittest.TestCase):

    def test_create_restaurant(self):
        restaurant = Restaurant.create(name="restaurant name", address="address 1", food="seafood", user_id=1)
        self.assertEqual(restaurant.name, "restaurant name")
        self.assertEqual(restaurant.user_id, 1)

    def test_create_table(self):
        restaurant = Restaurant.create(name="restaurant name", user_id=1)
        table = Table.create(name="table 1", capacity=4, minimum=2, restaurant_id=restaurant.id)
        self.assertEqual(table.restaurant_id, restaurant.id)
