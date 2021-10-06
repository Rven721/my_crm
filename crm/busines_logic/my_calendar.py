from datetime import date


def get_request_date(request_date):
    try:
        year = int(request_date[0:4])
        month = int(request_date[5:7])
        day = int(request_date[8:])
    except (ValueError, TypeError):
        today = date.today()
        year = today.year
        month = today.month
        day = today.day
    result = {
        'year': year,
        'month': month,
        'day': day,
    }
    return result
