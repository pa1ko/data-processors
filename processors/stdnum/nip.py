# -*- coding: utf-8 -*-
"""Extrac information from Polish Tax Identifiaction Number - NIP."""

from processors import generic


def unify(items):
    """Unify NIP number."""
    if items.dtype != 'O':
        items = items.apply(str)

    items = (items.str.strip()
             .str.lower()
             .str.replace('pl|-| ', ''))

    return items


def is_valid(items):
    """Bool mask with True if nip is valid."""
    nip_regex = r'^(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$'

    digit_df = generic.split_numbers_to_columns(items, nip_regex)

    controlsum = (
        6 * digit_df.iloc[:, 0].values +
        5 * digit_df.iloc[:, 1].values +
        7 * digit_df.iloc[:, 2].values +
        2 * digit_df.iloc[:, 3].values +
        3 * digit_df.iloc[:, 4].values +
        4 * digit_df.iloc[:, 5].values +
        5 * digit_df.iloc[:, 6].values +
        6 * digit_df.iloc[:, 7].values +
        7 * digit_df.iloc[:, 8].values
    ) % 11

    return digit_df.iloc[:, 9] == controlsum
