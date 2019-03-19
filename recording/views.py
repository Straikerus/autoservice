from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.shortcuts import render

from core.models import Specialist

from .utils import get_unallowed_days_dict, get_allowed_times_list
from .forms import RecordForm


class RecordingFormView(View):
    def get(self, request, *args, **kwargs):
        form = RecordForm()
        return render(request, 'recording-form.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Вы успешно записались')
        return render(request, 'recording-form.html', {'form': form})


class UnavailableDaysView(View):
    def get(self, request, *args, **kwargs):
        try:
            specialist = Specialist.objects.get(id=request.GET.get('specialist'))
        except Specialist.DoesNotExist:
            return JsonResponse({'error': 'Специалист не существует'}, status=400)
        unallowed_days = get_unallowed_days_dict(specialist)
        return JsonResponse({'unavailableDaysJson': unallowed_days})


class AvailableTimeOptionsView(View):
    def get(self, request, *args, **kwargs):
        specialist = Specialist.objects.get(id=request.GET.get('specialist'))
        times_list = get_allowed_times_list(specialist, request.GET.get('date'))
        if times_list:
            html_options = render_to_string(
                'components/time-options.html',
                {'times': times_list}
            )
            return JsonResponse({'options': html_options})
        return JsonResponse({'error': 'В выбранный день нет доступного времени'})
