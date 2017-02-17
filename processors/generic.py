# -*- coding: utf-8 -*-
"""Generic funcs."""
import pandas as pd


# Broadcast
def broadcast_to(series, to):
    """Align series to shape of other, similiar to numpy broadcast.

    To align few rules must be meet:
    - longer must have len that is multiplication of short one
    - data in short one is multiplication of its own data
    - no index data is preserved or copied
    """
    if len(to) % len(series) == 0:
        return pd.Series((series.repeat(len(to)/len(series))).values)
    else:
        raise ValueError('Cannot broadcast Series, shape not align: [{},], [{},]'.format(len(series), len(to)))


def align_series(series1, series2):
    """Check length of series and try align them against each other.

    It will try align shorter series to longer, it must meet all rulse
    of function broadcast_to.

    Return two element tuple (series1, series2)
    """
    if len(series1) > len(series2):
        return series1, broadcast_to(series2, series1)
    elif len(series1) < len(series2):
        return broadcast_to(series1, series2), series2
    else:
        return series1, series2


# Checksum
def split_numbers_to_columns(series, pattern):
    """Split given series to columns with given regex.

    Each columns will be following numbers in series.
    """
    return (series.str.extract(pattern, expand=True)
            .applymap(float))  # float because of posible NaN's
