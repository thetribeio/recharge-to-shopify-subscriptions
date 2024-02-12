from datetime import datetime


def transform_cadence(cadence_interval, cadence_interval_count):
    if cadence_interval == 'day':
        days = int(cadence_interval_count)
        if days % 30 == 0:
            return 'month', days // 30
        elif days % 7 == 0:
            return 'week', days // 7
        else:
            return 'week', days // 7
    elif cadence_interval == 'month':
        return 'month', int(cadence_interval_count)
    elif cadence_interval == 'week':
        return 'week', int(cadence_interval_count)
    else:
        return cadence_interval, int(cadence_interval_count)


def extract_id_from_token(token):
    try:
        return token.split('/')[-1]
    except IndexError:
        return None


def format_iso8601(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_date
