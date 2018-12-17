#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" Run all tests """

import unittest

loader = unittest.TestLoader()
suite = loader.discover('tests')

runner = unittest.TextTestRunner()
runner.run(suite)
