# -*- coding: utf-8 -*-
"""Generic funcs."""
import pandas as pd


def broadcast_to(series, to):
    """Try to align two Series, similiar to numpy broadcast.

    Short one is along long-one, similiar len takes no efect and also
    longer one must be multiplication of shorter. No index informations
    are preserved. Shorter repeated data.
    """
    if len(to) % len(series) == 0:
        return pd.Series((series.repeat(len(to)/len(series))).values)
    else:
        raise ValueError('Cannot broadcast Series, shape not align: [{},], [{},]'.format(len(series), len(to)))


def align_series(series1, series2):
    """Check length of series and try align them against each other.

    It will try shorter series align longer, same rule as for function
    broadcast_to.
    """
    if len(series1) > len(series2):
        return series1, broadcast_to(series2, series1)
    elif len(series1) < len(series2):
        return broadcast_to(series1, series2), series2
    else:
        return series1, series2
