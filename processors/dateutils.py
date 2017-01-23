# -*- coding: utf-8 -*-
"""Module to help in date/time manipulation."""
from datetime import datetime
import pandas as pd


def unify(date):
    """Ensure that data will be return in unifed format.

    That means Series with datetime objects (without time grain).
    """
    if isinstance(date, str):
        s = pd.Series([pd.to_datetime(date)])
    elif isinstance(date, datetime):
        s = pd.Series([date])
    elif isinstance(date, pd.Series) and date.dtype != datetime:
        s = pd.to_datetime(date)
    else:
        raise NotImplementedError

    return s.dt.normalize()

def datediff(date1, date2, interval):
    """Return date difference on given interval. Diff is in full units.

    Avalible intervals:
        D - day
        M - month
        Y - year
    """
    if interval == 'D':
        return (date1 - date2).dt.days
    elif interval == 'M':
        return ((date1.dt.month - date2.dt.month)
                + (date1.dt.year - date2.dt.year) * 12)
    elif interval == 'Y':
        return date1.dt.year - date2.dt.year
    else:
        raise ValueError('Unknown interval {}'.format(interval))
