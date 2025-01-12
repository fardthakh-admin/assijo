# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from rest_framework import routers

from apps.home import views
from .views import download_weather_csv


urlpatterns = [

    # The home page
    path('home/', views.index, name='home'),
    # path('', views.weather_station, name='WS'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('base-fullscreen', views.title_view, name='base-fullscreen'),
    path('sensor', views.sensor_view, name='sensor'),
    path('valve', views.valve_view, name='valve'),
    path('tree', views.tree_view, name='tree'),
    path('water_pump', views.water_pump_view, name='water_pump'),
    path('water_tank', views.water_tank_view, name='water_tank'),
    path('users', views.users_view, name='users'),
    path('offline_scenario', views.offline_scenario_view, name='offline_scenario'),
    path('weather_station', views.WeatherStationView.as_view(), name='weather_station'),
    path('weather_station_past', views.WeatherStationPastView.as_view(), name='weather_station_past'),
  



    path('create_farm', views.create_farm, name = "create_farm" ),
    path('create_farm_borders', views.create_farm_borders, name = "create_farm_borders" ),
    path('create-user', views.UserOperation.as_view(), name = "create-user" ),
    path('mydata_sensor',views.mydata_sensor, name="mydata_sensor"),
    path('mydata_valve',views.mydata_valve, name="mydata_valve"),
    path('mydata_waterpump',views.mydata_waterpump, name="mydata_waterpump"),
    path('mydata_watertank',views.mydata_watertank, name="mydata_watertank"),
    path('mydata_Trees',views.mydata_Trees, name="mydata_Trees"),
    path('mydata_weatherstation',views.mydata_weatherstation, name="mydata_weatherstation"),

    path('api/weather_station', views.WeatherStationAPI.as_view(), name='weather_station_api'),

    path('api/delete/sensor/', views.DeleteSensor.as_view(), name='delete-sensor_api'),
    path('api/delete/valve/', views.DeleteValve.as_view(), name='delete-valve_api'),
    path('api/delete/tree/', views.DeleteTree.as_view(), name='delete-tree_api'),
    path('api/delete/water_pump/', views.DeleteWaterPump.as_view(), name='delete-water_pump_api'),
    path('api/delete/water_tank/', views.DeleteWaterTank.as_view(), name='delete-water_tank_api'),
    path('api/delete/weather_station/', views.DeleteWeatherstation.as_view(), name='delete-weather_station_api'),

    path('api/delete/offline_scenario/', views.DeleteOfflineScenario.as_view(), name='delete-offline_scenario_api'),

    path('watertank-operation/', views.WaterTankOperation.as_view(), name='watertank-operation'),
    path('sensor-operation/', views.SensorOperation.as_view(), name='sensor-operation'),
    path('valve-operation/', views.ValveOperation.as_view(), name='valve-operation'),
    path('WeatherStation-operation/', views.WeatherStationOperation.as_view(), name='WeatherStation-operation'),
    path('tree-operation/', views.TreeOperation.as_view(), name='tree-operation'),
    path('waterpump-operation/', views.WaterPumpOperation.as_view(), name='waterpump-operation'),
    path('offlinescenario-operation/', views.OfflineScenarioOperation.as_view(), name='offlinescenario-operation'),
     path('download-weatherStaionResultsCSV/', download_weather_csv, name='download_weather_csv'),

    # path('water_tank', views.water_tank_view),

]
