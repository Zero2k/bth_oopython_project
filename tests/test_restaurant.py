import unittest

from app import db
from app.modules.restaurant.models import Restaurant, Table

class TestRestaurantModule(unittest.TestCase):

    def test_create_restaurant(self):
        restaurant = Restaurant.create(name="Restaurant Name")
        self.assertEqual(restaurant.name, "Restaurant Name")

    def test_create_table(self):
        restaurant = Restaurant.create(name="Restaurant Name")
        table = Table.create(capacity=4, minimum=2, restaurant_id=restaurant.id)
        self.assertEqual(table.restaurant_id, restaurant.id)
