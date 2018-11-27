import unittest

from app import db
from app.modules.auth.models import User

class TestAuthModule(unittest.TestCase):

    def test_user(self):
        user = User.get(1)
        self.assertEqual(user.name, "test")
