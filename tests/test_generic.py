# -- coding: utf-8 -*-
import unittest
from pandas import Series, DataFrame
from numpy import NaN
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


class TestAlignSeries(unittest.TestCase):

    def setUp(self):
        self.s1 = Series(['a', 'b', 'c'])
        self.s2 = Series(['d'])
        self.s3 = Series(['z', 'x', 'y'])
        self.s4 = Series(['u', 'u'])

    def test_align_brodcast_right(self):
        ns1, ns2 = generic.align_series(self.s1, self.s2)
        assert len(ns1) == len(ns2), 'diff length'
        pdtest.assert_series_equal(ns2, Series(['d', 'd', 'd']),
                                   check_names=False)

    def test_align_brodcast_left(self):
        ns2, ns3 = generic.align_series(self.s2, self.s3)
        assert len(ns2) == len(ns3), 'diff length'
        pdtest.assert_series_equal(ns2, Series(['d', 'd', 'd']),
                                   check_names=False)

    def test_align_same_len(self):
        ns1, ns3 = generic.align_series(self.s1, self.s3)
        assert len(ns1) == len(ns3), 'diff length'
        pdtest.assert_series_equal(ns1, self.s1, check_names=False)
        pdtest.assert_series_equal(ns3, self.s3, check_names=False)

    def test_invalid_align(self):
        with self.assertRaises(ValueError):
            generic.align_series(self.s3, self.s4)


class TestSplitNumbersFunc(unittest.TestCase):

    def test_split_correct(self):
        tested = Series(['123', '456', '789', '12', '1234'])
        result = DataFrame([(1., 2., 3.),
                            (4., 5., 6.),
                            (7., 8., 9.),
                            (NaN, NaN, NaN),
                            (NaN, NaN, NaN)], columns=[0, 1, 2])

        pdtest.assert_frame_equal(
            generic.split_numbers_to_columns(tested, r'^(\d)(\d)(\d)$'),
            result
        )
