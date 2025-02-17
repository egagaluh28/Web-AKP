# traffic/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.traffic_form, name='traffic_form'),
    path('data/', views.traffic_data, name='traffic_data'),
    path('density/', views.traffic_density_view, name='traffic_density'),
]