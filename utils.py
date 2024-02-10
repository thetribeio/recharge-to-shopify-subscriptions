from datetime import datetime


def transform_cadence(order_interval_unit, order_interval_frequency):
    if order_interval_unit == 'day':
        days = int(order_interval_frequency)
        if days % 30 == 0:
            return 'month', days // 30
        elif days % 7 == 0:
            return 'week', days // 7
        else:
            return 'week', days // 7
    elif order_interval_unit == 'month':
        return 'month', int(order_interval_frequency)
    elif order_interval_unit == 'week':
        return 'week', int(order_interval_frequency)
    else:
        return order_interval_unit, int(order_interval_frequency)


def extract_id_from_token(token):
    try:
        return token.split('/')[-1]
    except IndexError:
        return None


def format_iso8601(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_date
