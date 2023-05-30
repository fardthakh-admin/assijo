from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.home import models
from . import serializers

@api_view(['GET'])
def api_over_view(request):
    api_urls = {
        'Farm' : '/farm/<int:id>',
        'Users': '/farm-users/<int:id>',
        'Sensors': '/farm-sensors/<int:id>',
        'Valves': '/farm-valves/<int:id>',
        'Water-Tanks': '/farm-water-tanks/<int:id>',
        'Water-Pumps': '/farm-water-pumps/<int:id>',
        'Energy-Levels': '/farm-energy-levels/<int:id>',
        'Results': '/farm-reading-results/<int:id>',
        'String-Results': '/farm-string-results/<int:id>',
        'Offline-Scenarios': 'farm-offline-scenarios/<int:id>/',
        'Gate-Way': 'farm-gate-way/<int:id>/',
        'Trees': 'farm-trees/<int:id>/',
        'Water-Share': 'farm-water-share/<int:id>/',
        'Weather-Station': 'farm-weather-station/<int:id>/',
        'Packet-Result': 'farm-packet-result/<int:id>/',


        'create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
    }
    return Response(api_urls)


### DATA VIEWING SECTION ###
@api_view(['GET'])
def farm_details( request, id ):
    farm = models.Farm.objects.get( id = id )
    serializer = serializers.FarmSerializer(farm, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def farm_users(request, id):
    users = models.User.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_sensors(request, id):
    sensors = models.Sensor.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.SensorSerializer(sensors, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_valves(request, id):
    valves = models.Valve.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.ValveSerializer(valves, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_water_tanks(request, id):
    water_tanks = models.WaterTank.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.WaterTankSerializer(water_tanks, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_water_pumps(request, id):
    water_pumps = models.WaterPump.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.WaterPumpSerializer(water_pumps, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_energy_levels(request, id):
    energy_levels = models.EnergyLevel.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.EnergyLevelSerializer(energy_levels, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_reading_results(request, id):
    results = models.Result.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.ResultSerializer(results, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_string_results(request, id):
    string_results = models.StringResult.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.StringResultSerializer(string_results, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_offline_scenario(request, id):
    offline_scenario = models.OfflineScenario.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.OfflineScenarioSerializer(offline_scenario, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_gate_way(request, id):
    gate_way = models.Gateway.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.GatewaySerializer(gate_way, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_trees(request, id):
    trees = models.Tree.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.TreeSerializer(trees, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_water_share(request, id):
    water_share = models.WaterShare.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.WaterShareSerializer(water_share, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_weather_station(request, id):
    weather_station = models.WeatherStation.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.WeatherStationSerializer(weather_station, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def farm_packet_results(request, id):
    packet_results = models.PacketResult.objects.filter(farm_id = id).order_by('-id')
    serializer = serializers.PacketResultSerializer(packet_results, many = True)
    return Response(serializer.data)
