# -- coding: utf-8 -*-
import unittest
from pandas import Series
import pandas.util.testing as pdtest

from processors import generic


class TestBroadcast(unittest.TestCase):

    def setUp(self):
        self.s1 = Series([1, 2, 3])
        self.s2 = Series([3, 2, 1])
        self.s3 = Series([6, 6])
        self.s4 = Series([10])

    def test_broadcast_short_long(self):
        pdtest.assert_series_equal(generic.broadcast_to(self.s4, self.s1),
                                   Series([10, 10, 10]),
                                   check_names=False)

    def test_broadcast_same_len(self):
        pdtest.assert_series_equal(generic.broadcast_to(self.s1, self.s2),
                                   self.s1,
                                   check_names=False)

    def test_broadcast_incorect_shape(self):
        with self.assertRaises(ValueError):
            generic.broadcast_to(self.s3, self.s1)
