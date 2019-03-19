from django.db import models

from core.models import Specialist, CarModel
from .validators import validate_not_before_today, validate_not_dayoff


class Record(models.Model):
    client = models.CharField('ФИО клиента', max_length=500)
    car_model = models.ForeignKey(
        CarModel,
        verbose_name='Марка автомобиля',
        on_delete=models.CASCADE
    )
    specialist = models.ForeignKey(
        Specialist,
        verbose_name='Специалист',
        on_delete=models.CASCADE
    )
    datetime = models.DateTimeField(
        'Время записи',
        validators=[validate_not_before_today, validate_not_dayoff],
    )

    def __str__(self):
        return '{} к {} с автомобилем {}. Дата и время: {}'.format(
            self.client,
            self.specialist.get_full_name(),
            self.car_model.name,
            self.datetime.strftime("%d-%m-%Y %H:%M")
        )
    
    class Meta:
        verbose_name = 'Запись на диагностику'
        verbose_name_plural = 'Записи на диагностику'
