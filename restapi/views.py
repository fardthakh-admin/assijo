from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.home import models
import numpy as np
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
        'Sensor-Humidity-Results': '/farm-humidity-results/',
        'Timestamps': '/farm-timestamps/',
        'Water-Tanks': '/farm-water-level-results/',
        'Water-Share': 'farm-water-share/',
        'Valve-Flow-Results': '/farm-valveflow-results/',
        'String-Results': '/farm-string-results/',
        'Offline-Scenarios': 'farm-offline-scenarios/',
        'Gate-Way': 'farm-gate-way/',
        'Trees': 'farm-trees/',
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
def farm_timestamps(request):
    user = models.User.objects.get(id = request.user.id)
    sensors = models.Sensor.objects.filter(farm_id=user.farm)

    list_of_timestamps = []

    results = models.Result.objects.filter(sensor__farm = user.farm).order_by('timestamp').values('number', 'timestamp')
    for result in results:
        list_of_timestamps.append(result['timestamp'].strftime('%Y-%m-%d'))

    list_of_timestamps = np.unique(list_of_timestamps)
    return Response(list_of_timestamps)


@api_view(['GET'])
def farm_energy_levels(request):
    user = models.User.objects.get(id = request.user.id)

    waterpumps = models.WaterPump.objects.filter(farm_id=user.farm)

    # Create a list to store the data
    data = []
    for pump in waterpumps:
        # Get the WaterTank ID from the water tank
        pump_id = pump.id

        # Get the list of water level results for the current water tank
        energy_level_result = list(models.Result.objects.filter(water_pump__id=pump_id).values_list('number', flat=True))
        energy_level_result = list(map(int, energy_level_result))

        # Get the unit for the current water tank from the first result (assuming same unit for all results)
        results = models.Result.objects.filter(water_pump__id=pump.id)
        unit = results[0].unit if results.exists() and results[0].unit else None

        # Create a dictionary for the current water tank and append it to the data list
        data.append({
            'Water_pump_id': pump_id,
            'unit': unit,
            'energy_levels': energy_level_result,
        })

    return Response(data)


    ### OLD CODE
    # user = models.User.objects.get(id = request.user.id)
    # waterpumps = models.WaterPump.objects.filter(farm_id=user.farm)
    # energy_levels = models.EnergyLevel.objects.filter(water_pump__in = waterpumps).order_by('-id')
    # serializer = serializers.EnergyLevelSerializer(energy_levels, many = True)
    # data = serializer.data

    # energy_level_result_list = []
    
    # for result in data:
    #     # energy_level = list(models.EnergyLevel.objects.filter(water_pump__id = result.id).values_list('number', flat=True))
    #     energy_level_result_list.append(int(result["energy_result"]))


    # list_of_energy_level_results = []

    # for pump in waterpumps:
    #     pump_energy_level_results = list(models.EnergyLevel.objects.filter(water_pump__id = pump.id).values_list('energy_result', flat=True))
    #     pump_energy_level_results = list(map(int, pump_energy_level_results))
    #     list_of_energy_level_results.append(pump_energy_level_results)

    # return Response(list_of_energy_level_results)


@api_view(['GET'])
def farm_humidity_results(request):
    user = models.User.objects.get(id = request.user.id)

    sensors = models.Sensor.objects.filter(farm_id=user.farm)

    # Create a list to store the data
    data = []
    for sensor in sensors:
        # Get the WaterTank ID from the water tank
        sensor_id = sensor.id

        # Get the list of water level results for the current water tank
        humidity_result = list(models.Result.objects.filter(sensor__id=sensor.id).values_list('number', flat=True))
        humidity_result = list(map(int, humidity_result))

        # Get the unit for the current water tank from the first result (assuming same unit for all results)
        results = models.Sensor.objects.filter(id=sensor.id)
        unit = results[0].unit if results.exists() and results[0].unit else None

        # Create a dictionary for the current water tank and append it to the data list
        data.append({
            'sensor_id': sensor_id,
            'unit': unit,
            'humidity': humidity_result,
        })

    return Response(data)


    ### OLD CODE
    # user = models.User.objects.get(id = request.user.id)
    # sensors = models.Sensor.objects.filter(farm_id=user.farm)
    # results = models.Result.objects.filter(sensor__in = sensors).order_by('-id')
    # serializer = serializers.ResultSerializer(results, many = True)
    
    # list_of_humidity_results = []

    # for sensor in sensors:
    #     humidity_result = list(models.Result.objects.filter(sensor__id = sensor.id).values_list('number', flat=True))
    #     humidity_result = list(map(int, humidity_result))
    #     list_of_humidity_results.append(humidity_result)

    # return Response(list_of_humidity_results)


@api_view(['GET'])
def farm_water_level_results(request):
    user = models.User.objects.get(id = request.user.id)

    water_tanks = models.WaterTank.objects.filter(farm_id=user.farm)

    # Create a list to store the data
    data = []
    for tank in water_tanks:
        # Get the WaterTank ID from the water tank
        watertank_id = tank.id

        # Get the list of water level results for the current water tank
        water_level_result = list(models.Result.objects.filter(water_tank__id=tank.id).values_list('number', flat=True))
        water_level_result = list(map(int, water_level_result))

        # Get the unit for the current water tank from the first result (assuming same unit for all results)
        results = models.Result.objects.filter(water_tank__id=tank.id)
        unit = results[0].unit if results.exists() and results[0].unit else None

        # Create a dictionary for the current water tank and append it to the data list
        data.append({
            'watertank_id': watertank_id,
            'unit': unit,
            'water_levels': water_level_result,
        })

    return Response(data)

    ### OLD CODE
    # water_tanks = models.WaterTank.objects.filter(farm_id = user.farm)

    # list_of_water_level_results = []

    # for tank in water_tanks:
    #     water_level_result = list(models.Result.objects.filter(water_tank__id = tank.id).values_list('number', flat=True))
    #     water_level_result = list(map(int, water_level_result))
    #     list_of_water_level_results.append(water_level_result)

    # return Response(list_of_water_level_results)


@api_view(['GET'])
def farm_water_share(request):
    # Get the authenticated user
    user = models.User.objects.get(id = request.user.id)

    # Filter trees based on the user's farm
    trees = models.Tree.objects.filter(farm_id=user.farm)

    # Filter water shares for the trees and order by ID in descending order
    water_share = models.WaterShare.objects.filter(tree__in=trees).order_by('-id')

    # Create a dictionary to store the data grouped by tree ID and unit
    data_by_tree_id = {}
    for share in water_share:
        tree_id = share.tree.id
        if share.unit:
            unit = share.unit
            key = f"{tree_id}_{unit}"
            if key not in data_by_tree_id:
                data_by_tree_id[key] = {
                    'tree_id': tree_id,
                    'unit': unit,
                    'shares': [],
                }
        else:
            key = f"{tree_id}_None"
            if key not in data_by_tree_id:
                data_by_tree_id[key] = {
                    'tree_id': tree_id,
                    'shares': [],
                }
        data_by_tree_id[key]['shares'].append(share.number)

    # Convert the dictionary values to a list to match the desired output format
    data = list(data_by_tree_id.values())

    return Response(data)

    # user = models.User.objects.get(id = request.user.id)
    # trees = models.Tree.objects.filter(farm_id=user.farm)
    # water_share = models.WaterShare.objects.filter(tree__in = trees).order_by('-id')
    # serializer = serializers.WaterShareSerializer(water_share, many = True)
    # data = serializer.data

    # for result in data:
    #     water_share_results = list(models.WaterShare.objects.filter(tree__id = tree.id).values_list('number', flat=True))
    #     print(result)

    # list_of_water_share_results = []

    # for tree in trees:
    #     water_share_results = list(models.WaterShare.objects.filter(tree__id = tree.id).values_list('number', flat=True))
    #     water_share_results = list(map(int, water_share_results))
    #     list_of_water_share_results.append(water_share_results)


    # return Response(list_of_water_share_results)


@api_view(['GET'])
def farm_valveflow_results(request):
    user = models.User.objects.get(id = request.user.id)

    Valves = models.Valve.objects.filter(farm_id=user.farm)

    # Create a list to store the data
    data = []
    for valve in Valves:
        # Get the WaterTank ID from the water tank
        valve_id = valve.id

        # Get the list of water level results for the current water tank
        valve_flow_result = list(models.Result.objects.filter(valve__id=valve.id).values_list('number', flat=True))
        valve_flow_result = list(map(int, valve_flow_result))

        # Get the unit for the current water tank from the first result (assuming same unit for all results)
        results = models.Result.objects.filter(valve__id=valve.id)
        unit = results[0].unit if results.exists() and results[0].unit else None

        # Create a dictionary for the current water tank and append it to the data list
        data.append({
            'valve_id': valve_id,
            'unit': unit,
            'valve_flow_results': valve_flow_result,
        })

    return Response(data)

    # user = models.User.objects.get(id = request.user.id)
    # valves = models.Valve.objects.filter(farm_id=user.farm)
    # results = models.Result.objects.filter(valve__in = valves).order_by('-id')
    # serializer = serializers.ResultSerializer(results, many = True)

    # list_of_valve_flow_results = []

    # for valve in valves:
    #     valve_flow_results = list(models.Result.objects.filter(valve__id = valve.id).values_list('number', flat=True))
    #     valve_flow_results = list(map(int, valve_flow_results))
    #     list_of_valve_flow_results.append(valve_flow_results)
    
    # return Response(list_of_valve_flow_results)


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