from django.conf import settings
from django import forms

from .models import Record


class RecordForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        input_formats=('%d.%m.%Y %H:%M',),
        widget=forms.HiddenInput()
    )
    class Meta:
        model = Record
        fields = '__all__'
