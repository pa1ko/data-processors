# -*- coding: utf-8 -*-
"""Module to help in dates manipulation."""
from datetime import datetime
import pandas as pd

from processors.generic import align_len

def unify(date):
    """Ensure that data will be return in unifed format.

    That means Series with datetime objects (without time grain) for
    lists/series also for scalars then len == 1.
    """
    if not isinstance(date, pd.Series):
        date = pd.Series(date)

    return pd.to_datetime(date, errors='coerce').dt.normalize()


def datediff(date1, date2, interval):
    """Return date difference on given interval. Diff is in full units.
    It accepts series and scalars that can be parsed by pandas
    to_datetime method.

    Avaliable intervals:
        D - day
        M - month
        Y - year
    """
    date1 = unify(date1)
    date2 = unify(date2)

    if len(date1) != len(date2):
        date1, date2 = align_len(date1, date2)

    if interval == 'D':
        return (date1 - date2).dt.days
    elif interval == 'M':
        return ((date1.dt.month - date2.dt.month)
                + (date1.dt.year - date2.dt.year) * 12)
    elif interval == 'Y':
        return date1.dt.year - date2.dt.year
    else:
        raise ValueError('Unknown interval {}'.format(interval))
