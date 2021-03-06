# -- coding: utf-8 -*-
"""Extract information from Polish ID Number: PESEL."""
import pandas as pd

from processors import generic
from processors import dateutils


def unify(items):
    """Unifi format of pesel number."""
    if items.dtype != 'O':
        items = items.apply(str)

    return items.str.strip()


def is_valid(items):
    """"Bool mask with True if pesel is valid."""
    pesel_regex = r'^(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$'

    digit_df = generic.split_numbers_to_columns(items, pesel_regex)

    controlsum = (
        9 * digit_df.iloc[:, 0].values +
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


def gender(items, gender_sym=None):
    """Extract gender from pesel.

    Decode 10th number of pesel to return gender:
    on even women, odd on men.
    gender_sym: tuple ('Female symbol', 'Male symbol'), if None will return
     1 = Female, 2 = Male.
    """
    if gender_sym is None:
        gender_sym = (1, 2)

    gender_digit = dict(
        zip([str(x) for x in range(10)],
            [gender_sym[0] if x % 2 == 0 else gender_sym[1] for x in range(10)])
        )

    gender_s = (items.where(is_valid(items))
                .str.slice(start=9, stop=10)
                .map(gender_digit))
    return gender_s


def birth_date(items):
    """Extract birth date from pesel."""
    mth_century_substract = {
        '18': 80,
        '19': 0,
        '20': 20,
        '21': 40,
        '22': 60
    }

    vitems = (items.where(is_valid(items))
              .str.extract(pat=r'^(\d\d)(\d\d)(\d\d)', expand=True)
              .rename(columns={0: 'year', 1: 'month', 2: 'day'})
              .assign(month=lambda x: x['month'].apply(float))
              .assign(century=lambda x: pd.cut(x['month'],
                                               bins=[0, 12, 32, 52, 72, 92],
                                               labels=['19', '20', '21', '22', '18']))
              .assign(year=lambda x: x['century'].str.cat(x['year']))
              .assign(month=lambda x: x['month'] - x['century'].map(mth_century_substract))
             )

    return pd.to_datetime(vitems[['year', 'month', 'day']])


def age(items, ex_date):
    """Get person age based on the pesel and check date.

    Simillary to other date related funcs you can pass str, datetime
    or series. Function will try to broadcast scalars.
    """
    return dateutils.datediff(date1=dateutils.unify(ex_date),
                              date2=birth_date(items),
                              interval='Y')
