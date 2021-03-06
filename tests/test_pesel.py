# -*- coding: utf-8 -*-
import unittest
import pandas as pd
from numpy import nan as NaN
import pandas.util.testing as pdtest
from datetime import datetime

from processors.stdnum import pesel


class PeselTestCase(unittest.TestCase):

    def setUp(self):
        self.pesel_df = pd.DataFrame(
            # valid
            [('44112607890', 2, datetime(1944, 11, 26), True, 72.),
             ('70102108696', 2, datetime(1970, 10, 21), True, 46.),
             ('01320107989', 1, datetime(2001, 12, 1), True, 15.),
             ('99851201182', 1, datetime(1899, 5, 12), True, 117.),
             # invalid
             # too long
             ('998512011821', NaN, pd.NaT, False, NaN),
             # to short
             ('3301051236', NaN, pd.NaT, False, NaN),
             # wrong checksum
             ('70102108691', NaN, pd.NaT, False, NaN),
             ('10102108696', NaN, pd.NaT, False, NaN),
             ('123', NaN, pd.NaT, False, NaN)],
            columns=['pesel', 'gender', 'birth_date', 'valid', 'age20161231']
        )

    def test_pesel_validation(self):
        tested = pesel.is_valid(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['valid'],
                                   check_names=False)

    def test_unify(self):
        tdf = pd.DataFrame([(' 123  ', '123'),
                            ('123', '123'),
                            ('    123', '123')],
                           columns=['dirty', 'clean'])

        tested = pesel.unify(tdf['dirty'])
        pdtest.assert_series_equal(tested, tdf['clean'],
                                   check_names=False)

    def test_pesel_gender(self):
        tested = pesel.gender(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['gender'],
                                   check_names=False)

    def test_pesel_map_gender(self):
        tested = pesel.gender(pd.Series(['44112607890', '01320107989', '123']),
                              gender_sym=('F', 'M'))
        pdtest.assert_series_equal(tested, pd.Series(['M', 'F', NaN]),
                                   check_names=False)

    def test_pesel_birth_date(self):
        tested = pesel.birth_date(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['birth_date'],
                                   check_names=False)

    def test_pesel_age(self):
        tested = pesel.age(self.pesel_df['pesel'], '2016-12-31')
        pdtest.assert_series_equal(tested, self.pesel_df['age20161231'],
                                   check_names=False)

    def test_numeric_pesel(self):
        tested = pd.Series([44112607890], dtype='int64')
        pdtest.assert_series_equal(pesel.unify(tested),
                                   pd.Series(['44112607890']),
                                   check_names=False)

        assert tested.dtype == 'int64', 'Series type changed to: {}'.format(tested.dtype)
