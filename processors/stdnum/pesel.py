# -- coding: utf-8 -*-
"""
Extract information from Polish ID Number: PESEL.
"""
import logging
import datetime
from pandas import cut
from dateutil.relativedelta import relativedelta


# ===
# Regex pattern of correct pesel number
PESEL_REGEX = r'^(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$'
# Mapping 10th number of pesel to gender
GENDER_DIGIT = {
    '0': 'K',
    '2': 'K',
    '4': 'K',
    '6': 'K',
    '8': 'K',
    '1': 'M',
    '3': 'M',
    '5': 'M',
    '7': 'M',
    '9': 'M',
}
# Birth date correction agianst century
CENTURY_FACTORS = {
    18: -80,
    19: 0,
    20: -20,
    21: -40,
    22: -60
}


def format(s):
    """Unifi format."""
    return s.str.strip()


def is_valid(s):
    """"Bool mask with True as valid pesel."""
    digit_df = (s.str.extract(PESEL_REGEX, expand=True)
                .applymap(float)
               )

    controlsum = (9 * digit_df.iloc[:, 0].values +
                  7 * digit_df.iloc[:, 1].values +
                  3 * digit_df.iloc[:, 2].values +
                  1 * digit_df.iloc[:, 3].values +
                  9 * digit_df.iloc[:, 4].values +
                  7 * digit_df.iloc[:, 5].values +
                  3 * digit_df.iloc[:, 6].values +
                  1 * digit_df.iloc[:, 7].values +
                  9 * digit_df.iloc[:, 8].values +
                  7 * digit_df.iloc[:, 9].values
                 ) % 10

    return digit_df.iloc[:, 10] == controlsum


def gender(s):
    """Extract gender from pesel."""
    if s.dtype != 'O':
        s = s.apply(str)

    valid_mask = is_valid(s)

    return s[valid_mask].str.slice(start=9, stop=10).map(GENDER_DIGIT)


def birth_date(s):
    """Extract birth date from pesel."""
    if s.dtype != 'O':
        s = s.apply(str)

    new_s = s[is_valid(s)]
    new_s = (new_s.str.extract(pat=r'^(\d\d)(\d\d)(\d\d)', expand=True))
    new_s.columns = ['year', 'month', 'day']

    new_s = new_s.assign(year=lambda x: x['year'].astype(int),
                         month=lambda x: x['month'].astype(int),
                         day=lambda x: x['day'].astype(int))
    new_s = new_s.assign(century=lambda x: cut(x['month'],
                                               bins=[0, 12, 32, 52, 72, 92],
                                               labels=[19, 20, 21, 22, 18]))

    # TODO: dokonczyc...

    return new_s


def age(s, ex_date):
    """Get person age based on the pesel and second date."""
    return
