# -*- coding: utf-8 -*-
"""Extrac information from polish phone number."""


def unify(items):
    """Unify PL phone number to form: '123123123'."""
    if items.dtype != 'O':
        items = items.apply(str)

    re_pattern = r' |\(|\)|-|^\+48'
    items = (items.str.strip()
             .replace(re_pattern, '', regex=True)
             .replace('^0', '', regex=True)
            )
    return items


def verify(items):
    """Verify if number is correct."""
    return (items.str.len() == 9) & (items.str.isnumeric())


def tel_type(items):
    """Return 1 if phone is ground or 2 if cellphone."""
    ground_prefixes = ['12', '13', '14', '15', '16', '17', '18', '22', '23', '24',
                       '25', '29', '32', '33', '34', '41', '42', '43', '44', '46',
                       '48', '52', '54', '55', '56', '58', '59', '61', '62', '63',
                       '65', '67', '68', '71', '74', '75', '76', '77', '81', '82']

    map_pattern = dict(zip(ground_prefixes, [1 for _ in range(len(ground_prefixes))]))

    items = (items.str.slice(0, 2)
             .map(map_pattern)
             .fillna(2)
             .apply(int))

    return items
