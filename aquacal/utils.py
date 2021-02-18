from datetime import datetime
import requests


def is_weekend():
    today = datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return (today.weekday() > 4)


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None
