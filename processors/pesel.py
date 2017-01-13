# -- coding: utf-8 -*-
"""
Information extraction from Polish ID Number PESEL
"""

import logging
import datetime
from pandas import cut
from dateutil.relativedelta import relativedelta


def is_valid(s):
    """"Zwraca maske bool, czy numery pesel sa prawdziwe"""
    pesel_pattern = r'(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)'
    digit_df = s.str.extract(pesel_pattern, expand=True)
    for col in digit_df.columns:
        digit_df.loc[:, col] = digit_df[col].astype(float)

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
    """Wyciaga plci z numeru pesel"""
    gender_digit = {
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

    if s.dtype != 'O':
        s = s.astype(str)

    new_s = s[is_valid(s)]
    return new_s.str.slice(start=9, stop=10).map(gender_digit)


def birth(s):
    """Zwraca date urodzenia z numeru pesel"""
    century_factors = {
        18: -80,
        19: 0,
        20: -20,
        21: -40,
        22: -60
    }

    if s.dtype != 'O':
        s = s.astype(str)

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


def age(pesel, end_date=datetime.datetime.today()):
    """Wyciaga z peselu wiek klienta wzgledem roku kalendarzowego"""
    try:
        pesel = str(pesel)
        # assert len(pesel) == 11, 'Zla dlugosc numeru pesel'

        def get_ym(nr):
            nr = int(nr)
            if nr >= 81 and nr <= 92:
                c, m = 18 * 100, nr - 80
            elif nr >= 1 and nr <= 12:
                c, m = 19 * 100, nr
            elif nr >= 21 and nr <= 32:
                c, m = 20 * 100, nr - 20
            else:
                return None
            return c, m

        d = int(pesel[4:6])
        y_, m = get_ym(pesel[2:4])
        _y = int(pesel[0:2])
        y = y_ + _y
        y_diff = relativedelta(end_date, datetime.datetime(y, m, d)).years
        return y_diff

    except BaseException as e:
        logging.warning('Blad parsowania pesela %s: \n%s', pesel, e)
        return None
