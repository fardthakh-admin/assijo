from django.urls import path
from . import views

urlpatterns = [
    # Initial Path
    path('',views.api_over_view , name = 'api_over_view'),

    # Farm Urls
    path('farm/',views.farm_details , name = 'farm'),
    path('farm-users/',views.farm_users , name = 'farm-users'),
    path('farm-sensors/',views.farm_sensors , name = 'farm-sensors'),
    path('farm-valves/',views.farm_valves , name = 'farm-valves'),
    path('farm-water-tanks/',views.farm_water_tanks , name = 'farm-water-tanks'),
    path('farm-water-pumps/',views.farm_water_pumps , name = 'farm-water-pumps'),
    path('farm-timestamps/',views.farm_timestamps , name = 'farm-timestamps'),
    path('farm-energy-levels/',views.farm_energy_levels , name = 'farm-energy-levels'),
    path('farm-humidity-results/',views.farm_humidity_results , name = 'farm-humidity-results'),
    path('farm-water-level-results/',views.farm_water_level_results , name = 'farm-water-level-results'),
    path('farm-valveflow-results/',views.farm_valveflow_results , name = 'farm-valveflow-results'),
    path('farm-string-results/',views.farm_string_results , name = 'farm-string-results'),
    path('farm-offline-scenarios/',views.farm_offline_scenario , name = 'farm-offline-scenarios'),
    path('farm-gate-way/',views.farm_gate_way , name = 'farm-gate-way'),
    path('farm-trees/',views.farm_trees , name = 'farm-trees'),
    path('farm-water-share/',views.farm_water_share , name = 'farm-water-share'),
    path('farm-weather-station/',views.farm_weather_station , name = 'farm-weather-station'),
    path('farm-packet-results/',views.farm_packet_results , name = 'farm-packet-results'),
]