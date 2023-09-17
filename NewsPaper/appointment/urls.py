from django.urls import path, include

from .views import AppointmentView

app_name = 'appointment'

urlpatterns = [
    path('make_appointment/',
         AppointmentView.as_view(template_name='make_appointment.html'),
         name='make_appointment')]