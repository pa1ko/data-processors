# -*- coding: utf-8 -*-
"""Generic funcs."""
import pandas as pd


def broadcast_to(series, to):
    """Try to align two Series, similiar to numpy broadcast.

    Short one is along long-one, similiar len takes no efect and also
    longer one must be multiplication of shorter.
    """

    if len(to) % len(series) == 0:
        return pd.Series((series.repeat(len(to)/len(series))).values)
    else:
        raise ValueError('Cannot broadcast Series, shape not align: {}, {}'.format(len(series), len(to)))


def align_len(s1, s2):
    return
