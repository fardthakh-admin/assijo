from django.urls import path
from . import views

urlpatterns = [
    # Initial Path
    path('',views.api_over_view , name = 'api_over_view'),

    # Farm Urls
    path('farm/<int:id>/',views.farm_details , name = 'farm'),
    path('farm-users/<int:id>/',views.farm_users , name = 'farm-users'),
    path('farm-sensors/<int:id>/',views.farm_sensors , name = 'farm-sensors'),
    path('farm-valves/<int:id>/',views.farm_valves , name = 'farm-valves'),
    path('farm-water-tanks/<int:id>/',views.farm_water_tanks , name = 'farm-water-tanks'),
    path('farm-water-pumps/<int:id>/',views.farm_water_pumps , name = 'farm-water-pumps'),
    path('farm-energy-levels/<int:id>/',views.farm_energy_levels , name = 'farm-energy-levels'),
    path('farm-reading-results/<int:id>/',views.farm_reading_results , name = 'farm-reading-results'),
    path('farm-string-results/<int:id>/',views.farm_string_results , name = 'farm-string-results'),
    path('farm-offline-scenarios/<int:id>/',views.farm_offline_scenario , name = 'farm-offline-scenarios'),
    path('farm-gate-way/<int:id>/',views.farm_gate_way , name = 'farm-gate-way'),
    path('farm-trees/<int:id>/',views.farm_trees , name = 'farm-trees'),
    path('farm-water-share/<int:id>/',views.farm_water_share , name = 'farm-water-share'),
    path('farm-weather-station/<int:id>/',views.farm_weather_station , name = 'farm-weather-station'),
    path('farm-packet-results/<int:id>/',views.farm_packet_results , name = 'farm-packet-results'),
]