from django.db import models


class Specialist(models.Model):
    avatar = models.ImageField('Фото', blank=True, null=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True, null=True)

    def get_full_name(self):
        return '{} {} {}'.format(
            self.last_name,
            self.first_name,
            self.middle_name if self.middle_name else ''
        )

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'


class CarModel(models.Model):
    name = models.CharField('Название марки', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'
