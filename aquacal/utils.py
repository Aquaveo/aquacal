from datetime import datetime
import requests


def is_weekend():
    today = datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return today.weekday() > 4


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None


class AquaEvent:
    def __init__(self, name, date):
        self._name = name
        self.date = date

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, val):
        if not isinstance(val, datetime):
            raise ValueError("The date property must be a valid datetime object.")
        self._date = val

    def get_summary(self):
        return f'{self.name}: {self.date.strftime("%A, %B %D, %Y @ %I:%M %p")}'
