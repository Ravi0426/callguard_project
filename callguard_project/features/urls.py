from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('twilio/', views.twilio_callback, name='twilio_callback'),
    path('transcription/', views.transcription_callback, name='transcription_callback'),
]
