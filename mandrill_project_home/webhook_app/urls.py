from django.urls import path
from . import views

urlpatterns = [
    path('mandrill/', views.mandrill_events, name='mandrill_events'),
]
