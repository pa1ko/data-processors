# -*- coding: utf-8 -*-
import unittest
import pandas as pd
from numpy import nan as NaN
import pandas.util.testing as pdtest
from datetime import datetime

from processors.stdnum import nip


class PeselTestCase(unittest.TestCase):
    def setUp(self):
        self.nip_df = pd.DataFrame(
            [('7582043903', '7582043903', True),
             ('618-10-12-144', '6181012144', True),
             ('PL 6181012144', '6181012144', True),
             ('PL5541925947', '5541925947', True),
             (' 5541925947 ', '5541925947', True),
             # invalid
             ('PL123-445 ', '123445', False),
             ('7582043933', '7582043933', False),
             ('55419259471', '55419259471', False)
            ],
            columns=['nip', 'nip_unified', 'valid']
        )

    def test_unify(self):
        pdtest.assert_series_equal(nip.unify(self.nip_df['nip']),
                                   self.nip_df['nip_unified'],
                                   check_names=False)

    def test_validation(self):
        pdtest.assert_series_equal(nip.is_valid(self.nip_df['nip_unified']),
                                   self.nip_df['valid'],
                                   check_names=False)

    def test_numeric_validation(self):
        pdtest.assert_series_equal(nip.unify(pd.Series([7582043903])),
                                   pd.Series(['7582043903']),
                                   check_names=False)
