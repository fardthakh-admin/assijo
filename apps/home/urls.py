# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

    path('sensor', views.sensor_view, name='sensor'),
    path('valve', views.valve_view, name='valve'),
    path('tree', views.tree_view, name='tree'),
    path('water_pump', views.water_pump_view, name='water_pump'),
    path('water_tank', views.water_tank_view, name='water_tank'),
    path('weather_station', views.WeatherStationView.as_view(), name='weather_station'),
    path('api/weather_station', views.WeatherStationAPI.as_view(), name='weather_station_api'),
    path('api/delete/sensor/', views.DeleteSensor.as_view(), name='delete-sensor_api'),
    path('api/delete/valve/', views.DeleteValve.as_view(), name='delete-valve_api'),
    path('sensor-operation/', views.SensorOperation.as_view(), name='sensor-operation'),
    # path('water_tank', views.water_tank_view),

]
