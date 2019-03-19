from django.contrib import admin

from .models import Specialist, CarModel


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    pass


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    pass
