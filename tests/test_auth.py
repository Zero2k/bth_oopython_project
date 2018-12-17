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
