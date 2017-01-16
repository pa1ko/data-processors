# -*- coding: utf-8 -*-
import unittest
import pandas as pd
import pandas.util.testing as pdtest
from datetime import datetime

import processors.stdnum.pesel as pesel


class PeselTestCase(unittest.TestCase):

    def setUp(self):
        self.pesel_df = pd.DataFrame(
            [('44112607890', 'M', datetime(1944, 11, 26), True),
             ('70102108696', 'M', datetime(1970, 10, 21), True),
             ('01320107989', 'K', datetime(2001, 12, 1), True),
             ('99851201182', 'K', datetime(1899, 5, 12), True),
             ('70102108691', '-', pd.NaT, False),
             ('10102108696', '-', pd.NaT, False),
             ('123', '-', pd.NaT, False)],
            columns=['pesel', 'gender', 'birth_date', 'valid']
        )

    def test_pesel_validation(self):
        tested = pesel.is_valid(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['valid'],
                                   check_names=False)

    def test_pesel_gender(self):
        tested = pesel.gender(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['gender'],
                                   check_names=False)

    def test_pesel_birth(self):
        tested = pesel.birth_date(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['birth_date'],
                                   check_names=False)

    def test_pesel_age_full_years(self):
        tested = pesel.age(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['birth_date'],
                                   check_names=False)

    def test_pesel_age_day(self):
        tested = pesel.age(self.pesel_df['pesel'])
        pdtest.assert_series_equal(tested, self.pesel_df['birth_date'],
                                   check_names=False)
