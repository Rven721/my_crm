"""A modele to calculate nex and previous month"""


def get_next_period(year, month):
    """Will return next month and year for given date"""
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    next_period = {'year': next_year, 'month': next_month}
    return next_period


def get_prev_period(year, month):
    """Will return previous month and year for given date"""
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_period = {'year': prev_year, 'month': prev_month}
    return prev_period
