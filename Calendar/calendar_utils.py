def get_nearest_month(year, month):
    """Returns tuple of tuples: ((y_prev, m_prev), (y_next, m_next))"""
    if month == 12:
        next_ = (year + 1, 1)
        previous = (year, 11)
    elif month == 1:
        next_ = (year, 2)
        previous = (year - 1, 12)
    else:
        next_ = (year, month + 1)
        previous = (year, month - 1)
    return previous, next_