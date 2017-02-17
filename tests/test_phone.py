# -- coding: utf-8 -*-
import unittest
import pandas as pd
import pandas.util.testing as pdtest
from numpy import nan as NaN

from processors.stdnum import phone


class TestPhoneNumberPL(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            [('123123123', '123123123', True),
             ('(029)3123123', '293123123', True),
             ('+48123123123', '123123123', True),
             (' 293123123 ', '293123123', True),
             ('123-123-123', '123123123', True),
             ('123 123 123', '123123123', True),
             ('abcabcabc', 'abcabcabc', False),
             ('manuma', 'manuma', False)
            ], columns=['phone', 'phone_unifed', 'valid'])

    def test_unify(self):
        tested = phone.unify(self.df['phone'])
        pdtest.assert_series_equal(tested, self.df['phone_unifed'],
                                   check_names=False)

    def test_unify_numeric(self):
        numeric = pd.Series([123123123, 123123123])
        tested = phone.unify(numeric)
        pdtest.assert_series_equal(tested,
                                   numeric.apply(str),
                                   check_names=False)

    def test_verify(self):
        pdtest.assert_series_equal(phone.verify(self.df['phone_unifed']),
                                   self.df['valid'],
                                   check_names=False)

    def test_tel_type(self):
        tested = pd.Series(['606123123', '297654321'])
        pdtest.assert_series_equal(phone.tel_type(tested),
                                   pd.Series([2, 1]),
                                   check_names=False)
