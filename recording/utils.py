from datetime import datetime, timedelta
from django.conf import settings

from .models import Record

RECORDING_TIMES = []

def generate_times_list():
    """

    Генерация списка возможных для записи времён
    Пример списка ['10:00', '11:00', ..., '17:00']

    """
    time = int(settings.START_WORKING_TIME[:2]) * 60 + int(settings.START_WORKING_TIME[3:])
    end_time = int(settings.END_WORKING_TIME[:2]) * 60 + int(settings.END_WORKING_TIME[3:])
    while time <= end_time - settings.AVERAGE_DIAGNOSTICS_TIME:
        integer_part = str(time // 60)
        if len(integer_part) < 2:
            integer_part = '0' + integer_part
        fractional_part = str(time % 60)
        if len(fractional_part) < 2:
            fractional_part = '0' + fractional_part
        RECORDING_TIMES.append('{}:{}'.format(integer_part, fractional_part))
        time += settings.AVERAGE_DIAGNOSTICS_TIME

def get_unallowed_days_dict(specialist):
    """

    Генерация словаря с недоступными для записи днями
    Проверяются текущий и следующие 59 дней
    Словарь имеет вид {
        'месяц': [недоступные в этом месяце дни]
    }
    Пример словаря {
        '03': [2, 5, 7],
        '04': [10, 11, 12]
    }

    """
    unallowed_days = {}
    check_date = datetime.now()
    for day in range(60):
        records_count = Record.objects.filter(
                                            specialist = specialist,
                                            datetime__day = check_date.day,
                                            datetime__month = check_date.month,
                                            datetime__year = check_date.year
                                        ).count()
        if records_count >= len(RECORDING_TIMES):
            if check_date.month not in unallowed_days:
                unallowed_days[check_date.month] = []
            unallowed_days[check_date.month].append(check_date.day)
        check_date = check_date + timedelta(days = 1)
    return unallowed_days

def get_allowed_times_list(specialist, date):
    """

    Генерация списка с доступными для записи временами
    Пример списка ['10:00', '11:00']

    """
    allowed_times = []
    day, month, year = date.split('.')
    check_date = datetime(
        day = int(day),
        month = int(month),
        year = int(year),
        hour = int(settings.START_WORKING_TIME[:2]),
        minute = int(settings.START_WORKING_TIME[3:]),
    )
    for time in RECORDING_TIMES:
        try:
            record = Record.objects.get(
                                                specialist = specialist,
                                                datetime__day = check_date.day,
                                                datetime__month = check_date.month,
                                                datetime__year = check_date.year,
                                                datetime__hour = check_date.hour,
                                                datetime__minute = check_date.minute
                                            )
        except Record.DoesNotExist:
            allowed_times.append(time)
        check_date = check_date + timedelta(minutes = settings.AVERAGE_DIAGNOSTICS_TIME)
    if len(allowed_times) > 0:
        return allowed_times
    return False

# Запуск функции генерации списка возможных для записи времён
# Запускается 1 раз при запуске проекта
generate_times_list()
