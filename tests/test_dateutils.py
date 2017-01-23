# -- coding: utf-8 -*-
import unittest
from pandas import DataFrame, Series
from datetime import datetime, date
import pandas.util.testing as pdtest

from processors.dateutils import datediff, unify


class TestDateTimeParse(unittest.TestCase):

    def test_parse_str(self):
        dt_str = '2016-01-01 00:12:13'
        pdtest.assert_series_equal(unify(dt_str),
                                   Series([datetime(2016, 1, 1)]),
                                   check_names=False)

    def test_parse_datetime(self):
        dt_datetime = datetime(2020, 12, 1, 8, 3, 2)
        pdtest.assert_series_equal(unify(dt_datetime),
                                   Series([datetime(2020, 12, 1)]),
                                   check_names=False)

    def test_parse_date(self):
        dt_date = date(2020, 12, 1)
        pdtest.assert_series_equal(unify(dt_date),
                                   Series([datetime(2020, 12, 1)]))

    def test_parse_series_str(self):
        s_str = Series(['2010-01-01 12:00:00',])
        pdtest.assert_series_equal(unify(s_str),
                                   Series([datetime(2010, 1, 1)]),
                                   check_names=False)

    def test_parse_series_dtime(self):
        s_dt = Series([datetime(1987, 1, 1)])
        pdtest.assert_series_equal(unify(s_dt), s_dt, check_names=False)

class TestDateUtils(unittest.TestCase):

    def  test_raise_unknown_interval(self):
        with self.assertRaises(ValueError):
            datediff(Series([1]), Series([1]), interval='???')

    def test_round_datetime_to_days(self):
        df = DataFrame([
            (datetime(2000, 1, 1, 14, 13, 12), datetime(2000, 1, 1)),
            (datetime(2012, 12, 12, 23, 59, 59), datetime(2012, 12, 12))
        ], columns=['tested', 'expected'])

        pdtest.assert_series_equal(df['tested'], df['expected'],
                                   check_names=False)

    def test_day_dist(self):
        df = DataFrame([
            (datetime(2000, 1, 2), datetime(2000, 1, 1), 1),
            (datetime(2000, 1, 1), datetime(2000, 1, 2), -1),
            (datetime(2010, 1, 1), datetime(2000, 1, 1), 3653)
        ], columns=['d1', 'd2', 'diff'])

        pdtest.assert_series_equal(datediff(df['d1'], df['d2'], interval='D'),
                                   df['diff'],
                                   check_names=False)

    def test_param_str_datetime(self):
        raise NotImplementedError()
