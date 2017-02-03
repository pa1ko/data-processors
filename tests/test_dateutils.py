# -- coding: utf-8 -*-
import unittest
from pandas import DataFrame, Series, NaT
from datetime import datetime, date
import pandas.util.testing as pdtest

from processors import dateutils as dtu


class TestDateTimeParse(unittest.TestCase):

    def test_unify_cases_df(self):
        # floor datetime series
        df = DataFrame([
            (datetime(2000, 1, 1, 14, 13, 12), datetime(2000, 1, 1)),
            (datetime(2012, 12, 12, 23, 59, 59), datetime(2012, 12, 12))
        ], columns=['tested', 'expected'])

        pdtest.assert_series_equal(dtu.unify(df['tested']), df['expected'],
                                   check_names=False)

    def test_unify_cases_str(self):
        pdtest.assert_series_equal(dtu.unify('2017-01-01'),
                                   Series([datetime(2017, 1, 1)]),
                                   check_names=False)

        pdtest.assert_series_equal(dtu.unify('2017-01-01 12:11:10'),
                                   Series([datetime(2017, 1, 1)]),
                                   check_names=False)

    def test_unify_cases_date(self):
        pdtest.assert_series_equal(dtu.unify(date(2017, 1, 1)),
                                   Series([datetime(2017, 1, 1)]),
                                   check_names=False)

    def test_unify_cases_series_str(self):
        pdtest.assert_series_equal(dtu.unify(Series(['2017-01-01'])),
                                   Series([datetime(2017, 1, 1)]),
                                   check_names=False)

    def test_unify_cases_list_str(self):
        pdtest.assert_series_equal(dtu.unify(['2017-01-01', '2018-01-01']),
                                   Series([datetime(2017, 1, 1), datetime(2018, 1, 1)]),
                                   check_names=False)

    def test_unify_invalid_format(self):
        pdtest.assert_series_equal(dtu.unify(Series(['twelveoclock',])),
                                   Series([NaT,]),
                                   check_names=False)

    def test_parse_series_dtime(self):
        s_dt = Series([datetime(1987, 1, 1)])
        pdtest.assert_series_equal(dtu.unify(s_dt), s_dt, check_names=False)

    def test_nosideeffects(self):
        d_str = '2016-01-01'
        d_list = ['2016-01-01', '2016-01-01']
        d_s = Series(['2016-01-01'])

        dtu.unify(d_str)
        assert isinstance(d_str, str)

        dtu.unify(d_list)
        assert isinstance(d_list, list)

        dtu.unify(d_s)
        assert d_s.dtype == 'O'


class TestDatediff(unittest.TestCase):

    def setUp(self):
        self.df = DataFrame([
            (datetime(2000, 1, 2), datetime(2000, 1, 1), 1, 0, 0),
            (datetime(2000, 1, 1), datetime(2000, 1, 2), -1, 0, 0),
            (datetime(2010, 1, 1), datetime(2000, 1, 1), 3653, 120, 10),
            (datetime(2016, 2, 3), datetime(2016, 1, 1), 33, 1, 0)
        ], columns=['d1', 'd2', 'diff_d', 'diff_m', 'diff_y'])

    def  test_raise_unknown_interval(self):
        with self.assertRaises(ValueError):
            dtu.datediff(Series([1]), Series([1]), interval='???')

    def test_dist_day(self):
        pdtest.assert_series_equal(dtu.datediff(self.df['d1'], self.df['d2'], interval='D'),
                                   self.df['diff_d'],
                                   check_names=False)

    def test_dist_month(self):
        pdtest.assert_series_equal(dtu.datediff(self.df['d1'], self.df['d2'], interval='M'),
                                   self.df['diff_m'],
                                   check_names=False)

    def test_dist_year(self):
        pdtest.assert_series_equal(dtu.datediff(self.df['d1'], self.df['d2'], interval='Y'),
                                   self.df['diff_y'],
                                   check_names=False)

    def test_brodcast_date(self):
        dates_s = Series([datetime(2000, 1, 1), datetime(2001, 1, 1), datetime(2001, 2, 1)])

        pdtest.assert_series_equal(
            dtu.datediff(date1='2001-01-01', date2=dates_s, interval='D'),
            Series([366, 0, -31]),
            check_names=False)
