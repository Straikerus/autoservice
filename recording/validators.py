import datetime
from django.core.exceptions import ValidationError

def validate_not_before_today(value):
    if value.day < datetime.datetime.now().day:
        raise ValidationError('Дата должна быть не ранее сегодняшней')

def validate_not_dayoff(value):
    if value.weekday() in [5, 6]:
        raise ValidationError('Дата не должна выпадать на выходные дни')
