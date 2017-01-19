# -- coding: utf-8 -*-
"""Extract information from Polish ID Number: PESEL."""

import datetime
from pandas import cut
from dateutil.relativedelta import relativedelta

# ===
# Regex pattern of correct pesel number
PESEL_REGEX = r'^(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$'
# Birth date correction agianst century


def unify(items):
    """Unifi format of pesel number."""
    return items.str.strip()


def is_valid(items):
    """"Bool mask with True as valid pesel."""
    digit_df = (items.str.strip()
                .str.extract(PESEL_REGEX, expand=True)
                .applymap(float)  # float because of posible NaN's
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


def gender(items):
    """Extract gender from pesel.

    Decode 10th number of pesel to return gender:
    on even women odd on men TODO
    """
    gender_digit = dict(
        zip([str(x) for x in range(10)],
            ['K' if x % 2 == 0 else 'M' for x in range(10)])
        )

    if items.dtype != 'O':
        s = s.apply(str)

    valid_mask = is_valid(items)

    return s[valid_mask].str.slice(start=9, stop=10).map(gender_digit)


def birth_date(items):
    """Extract birth date from pesel."""

    century_factors = {
        18: -80,
        19: 0,
        20: -20,
        21: -40,
        22: -60
    }

    if items.dtype != 'O':
        s = s.apply(str)

    new_s = s[is_valid(items)]
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
