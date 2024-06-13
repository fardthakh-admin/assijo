from django.urls import path
from . import views

urlpatterns = [
    # Initial Path
    path("", views.api_over_view, name="api_over_view"),
    # Farm Urls
    # GET urls
    path("farm/", views.farm_details, name="farm"),
    path("farm-users/", views.farm_users, name="farm-users"),
    path("farm-sensors/", views.farm_sensors, name="farm-sensors"),
    path("farm-valves/", views.farm_valves, name="farm-valves"),
    path("farm-water-tanks/", views.farm_water_tanks, name="farm-water-tanks"),
    path("farm-water-pumps/", views.farm_water_pumps, name="farm-water-pumps"),
    path("farm-timestamps/", views.farm_timestamps, name="farm-timestamps"),
    path(
        "farm-timestamps-month/",
        views.farm_timestamps_month,
        name="farm-timestamps-month",
    ),
    path(
        "farm-timestamps-week/", views.farm_timestamps_week, name="farm-timestamps-week"
    ),
    path("farm-energy-levels/", views.farm_energy_levels, name="farm-energy-levels"),
    path(
        "farm-humidity-results/",
        views.farm_humidity_results,
        name="farm-humidity-results",
    ),
    path(
        "farm-water-level-results/",
        views.farm_water_level_results,
        name="farm-water-level-results",
    ),
    path(
        "farm-valveflow-results/",
        views.farm_valveflow_results,
        name="farm-valveflow-results",
    ),
    path("farm-string-results/", views.farm_string_results, name="farm-string-results"),
    path(
        "farm-offline-scenarios/",
        views.farm_offline_scenario,
        name="farm-offline-scenarios",
    ),
    path("farm-gate-way/", views.farm_gate_way, name="farm-gate-way"),
    path("farm-trees/", views.farm_trees, name="farm-trees"),
    path("farm-water-share/", views.farm_water_share, name="farm-water-share"),
    path(
        "farm-weather-station/", views.farm_weather_station, name="farm-weather-station"
    ),
    path("farm-packet-results/", views.farm_packet_results, name="farm-packet-results"),
    # POST urls
    path(
        "farm-create-sensor-result/<int:sensor_id>/",
        views.create_sensor_result,
        name="farm-create-sensor-result",
    ),
    path(
        "farm-create-packet-result/",
        views.create_packet_result,
        name="farm-create-packet-result",
    ),
    path(
        "farm-create-watertank-result/<int:watertank_id>/",
        views.create_watertank_result,
        name="farm-create-watertank-result",
    ),
    path(
        "farm-create-tree-result/<int:tree_id>/",
        views.create_tree_result,
        name="farm-create-tree-result",
    ),
    path(
        "farm-create-valve-result/<int:valve_id>/",
        views.create_valve_result,
        name="farm-create-valve-result",
    ),
    path(
        "farm-create-waterpump-result/<int:waterpump_id>/",
        views.create_waterpump_energylevel,
        name="farm-create-waterpump-result",
    ),
]
