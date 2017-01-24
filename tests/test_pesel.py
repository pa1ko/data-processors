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
            [('44112607890', 'M', datetime(1944, 11, 26), True),
             ('70102108696', 'M', datetime(1970, 10, 21), True),
             ('01320107989', 'K', datetime(2001, 12, 1), True),
             ('99851201182', 'K', datetime(1899, 5, 12), True),
             ('3301051236', NaN, pd.NaT, False),
             ('70102108691', NaN, pd.NaT, False),
             ('10102108696', NaN, pd.NaT, False),
             ('123', NaN, pd.NaT, False)],
            columns=['pesel', 'gender', 'birth_date', 'valid']
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

    def test_pesel_birth_date(self):
        tested = pesel.birth_date(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['birth_date'],
                                   check_names=False)

    def test_pesel_age(self):
        tested = pesel.age(self.pesel_df['pesel'], '2016-12-31')
        pdtest.assert_series_equal(tested, pd.Series([NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN]),
                                   check_names=False)
