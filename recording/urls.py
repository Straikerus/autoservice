from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecordingFormView.as_view(), name='recording-form'),
    path(
        'get-unallowed-days/',
        views.UnavailableDaysView.as_view(),
        name='get-unallowed-days'
    ),
    path(
        'get-allowed-time/',
        views.AvailableTimeOptionsView.as_view(),
        name='get-allowed-time'
    )
]
