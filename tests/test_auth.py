#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Test Auth Module
"""

import unittest

from app import db
from app.modules.auth.models import User

class TestAuthModule(unittest.TestCase):
    """ Test auth module and methods """

    def test_user(self):
        """ Get user with ID """
        user = User.get(1)
        self.assertEqual(user.name, "test")

    def test_change_user(self):
        """ Change user """
        user_data = User.get(1)

        user_data.name = "test20"
        user_data.email = "test20@test.com"

        User.update(user_data)

        updated_user = User.get(1)
        self.assertEqual(updated_user.name, "test20")
        self.assertEqual(updated_user.email, "test20@test.com")

        # Reset user
        updated_user.name = "test"
        updated_user.email = "test@test.com"

        User.update(updated_user)
