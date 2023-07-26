from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.home import models
from . import serializers

@api_view(['GET'])
def api_over_view(request):
    api_urls = {
        'Farm' : '/farm/',
        'Users': '/farm-users/',
        'Sensors': '/farm-sensors/',
        'Valves': '/farm-valves/',
        'Water-Tanks': '/farm-water-tanks/',
        'Water-Pumps': '/farm-water-pumps/',
        'Energy-Levels': '/farm-energy-levels/',
        'Results': '/farm-reading-results/',
        'String-Results': '/farm-string-results/',
        'Offline-Scenarios': 'farm-offline-scenarios/',
        'Gate-Way': 'farm-gate-way/',
        'Trees': 'farm-trees/',
        'Water-Share': 'farm-water-share/',
        'Weather-Station': 'farm-weather-station/',
        'Packet-Result': 'farm-packet-results/',
    }
    return Response(api_urls)


### DATA VIEWING SECTION ###
@api_view(['GET'])
def farm_details( request ):
    user = models.User.objects.get( id = request.user.id )
    farm = models.Farm.objects.get( owner = user.id )
    serializer = serializers.FarmSerializer(farm, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def farm_users( request ):
    logged_in_user = models.User.objects.get( id = request.user.id )
    users = models.User.objects.filter(farm_id = logged_in_user.farm).order_by('-id')
    serializer = serializers.UserSerializer(users, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_sensors( request ):
    user = models.User.objects.get(id = request.user.id)
    sensors = models.Sensor.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.SensorSerializer(sensors, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_valves( request ):
    user = models.User.objects.get(id = request.user.id)
    valves = models.Valve.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.ValveSerializer(valves, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_water_tanks(request):
    user = models.User.objects.get(id = request.user.id)
    water_tanks = models.WaterTank.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.WaterTankSerializer(water_tanks, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_water_pumps(request):
    user = models.User.objects.get(id = request.user.id)
    water_pumps = models.WaterPump.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.WaterPumpSerializer(water_pumps, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_energy_levels(request):
    user = models.User.objects.get(id = request.user.id)
    waterpumps = models.WaterPump.objects.filter(farm_id=user.farm)
    energy_levels = models.EnergyLevel.objects.filter(water_pump__in = waterpumps).order_by('-id')
    serializer = serializers.EnergyLevelSerializer(energy_levels, many = True)
    data = serializer.data

    energy_level_results = []
    

    for result in data:
        # energy_level = list(models.Result.objects.filter(sensor__id = result.id).values_list('number', flat=True))
        energy_level_results.append(int(result["energy_result"]))


    return Response(energy_level_results)


@api_view(['GET'])
def farm_reading_results(request):
    user = models.User.objects.get(id = request.user.id)
    sensors = models.Sensor.objects.filter(farm_id=user.farm)
    results = models.Result.objects.filter(sensor__in = sensors).order_by('-id')
    serializer = serializers.ResultSerializer(results, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_string_results(request):
    user = models.User.objects.get(id = request.user.id)
    sensors = models.Sensor.objects.filter(farm_id=user.farm)
    string_results = models.StringResult.objects.filter(sensors__in = sensors).order_by('-id')
    serializer = serializers.StringResultSerializer(string_results, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_offline_scenario(request):
    user = models.User.objects.get(id = request.user.id)
    offline_scenario = models.OfflineScenario.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.OfflineScenarioSerializer(offline_scenario, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_gate_way(request):
    user = models.User.objects.get(id = request.user.id)
    gate_way = models.Gateway.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.GatewaySerializer(gate_way, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_trees(request):
    user = models.User.objects.get(id = request.user.id)
    trees = models.Tree.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.TreeSerializer(trees, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_water_share(request):
    user = models.User.objects.get(id = request.user.id)
    trees = models.Tree.objects.filter(farm_id=user.farm)
    water_share = models.WaterShare.objects.filter(tree__in = trees).order_by('-id')
    serializer = serializers.WaterShareSerializer(water_share, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_weather_station(request):
    user = models.User.objects.get(id = request.user.id)
    weather_station = models.WeatherStation.objects.filter(farm_id = user.farm).order_by('-id')
    serializer = serializers.WeatherStationSerializer(weather_station, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def farm_packet_results(request):
    user = models.User.objects.get(id = request.user.id)
    weather_station = models.WeatherStation.objects.get(farm_id = user.farm).order_by('-id')
    packet_results = models.PacketResult.objects.filter(weather_station_id = weather_station.id).order_by('-id')
    serializer = serializers.PacketResultSerializer(packet_results, many = True)
    return Response(serializer.data)