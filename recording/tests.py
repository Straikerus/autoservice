import datetime
from django.test import TestCase
from django.conf import settings

# set test settings
settings.START_WORKING_TIME = '10:00'
settings.END_WORKING_TIME = '19:00'
settings.AVERAGE_DIAGNOSTICS_TIME = 60

from core.models import Specialist

from .models import Record, CarModel
from . import utils


class RecordingTestCase(TestCase):
    def setUp(self):
        date = datetime.datetime.now()
        self.date = date.replace(
            hour=10,
            minute=0,
            second=0,
            microsecond=0
        )
        self.specialist = Specialist.objects.create(
            first_name='Test',
            last_name='Testov'
        )
        self.car_model = CarModel.objects.create(name='BMW')
        self.record = Record.objects.create(
            client='Test client',
            car_model=self.car_model,
            specialist=self.specialist,
            datetime=self.date
        )

    def test_generating_times_list(self):
        times_list = [
            '10:00', '11:00', '12:00',
            '13:00', '14:00', '15:00',
            '16:00', '17:00', '18:00'
        ]
        self.assertEqual(times_list, utils.RECORDING_TIMES)

    def test_generating_unallowed_days(self):
        date_now = datetime.datetime.now()
        unallowed_days = {
            date_now.month: [date_now.day]
        }
        for i in range(len(utils.RECORDING_TIMES)):
            Record.objects.create(
                client='Test client',
                car_model=self.car_model,
                specialist=self.specialist,
                datetime=self.date
            )
        self.assertEqual(
            unallowed_days,
            utils.get_unallowed_days_dict(self.specialist)
        )
    
    def test_generating_allowed_times_list(self):
        allowed_times_list = [
            '11:00', '12:00', '13:00',
            '14:00', '15:00', '16:00',
            '17:00', '18:00'
        ]
        date_now = datetime.datetime.now()
        date_formatted = '{}.{}.{}'.format(
            date_now.day,
            date_now.month,
            date_now.year
        )
        self.assertEqual(
            allowed_times_list,
            utils.get_allowed_times_list(self.specialist, date_formatted)
        )
