import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
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
        'Timestamp-Month': '/farm-timestamps-month/',
        'Timestamp-Week': '/farm-timestamps-week/',
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
def farm_details(request):
    user = request.user
    farms = models.Farm.objects.filter(owner=user.id)
    if farms.exists():
        serializer = serializers.FarmSerializer(farms, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'No farm found for this user'}, status=status.HTTP_404_NOT_FOUND)


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

    start_date = request.query_params.get('start-date')
    end_date = request.query_params.get('end-date')
    
    if start_date is None:
        start_date = datetime.datetime.today() - datetime.timedelta(days=30)
    if end_date is None:
        end_date = datetime.datetime.today()
    
    results = models.Result.objects.filter(sensor__farm = user.farm , timestamp__range = (start_date, end_date)).order_by('timestamp').values('number', 'timestamp')
    
    return Response(results)

@api_view(['GET'])
def farm_timestamps_by_type(request, type):
    user = models.User.objects.get(id = request.user.id)
    sensor = models.Sensor.objects.filter(farm_id=user.farm, type=type)


    list_of_timestamps = []

    start_date = request.query_params.get('start-date')
    end_date = request.query_params.get('end-date')
    
    if start_date is None:
        start_date = datetime.datetime.today() - datetime.timedelta(days=30)
    if end_date is None:
        end_date = datetime.datetime.today()
    
    results = models.Result.objects.filter(sensor__id__in=sensor , timestamp__range = (start_date, end_date)).order_by('timestamp').values('number', 'timestamp')
    
    return Response(results)


@api_view(['GET'])
def farm_timestamps_days(request):
    user = models.User.objects.get(id = request.user.id)

    list_of_timestamps = []
        
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    
    results = models.Result.objects.filter(sensor__farm = user.farm , timestamp__range = (start_date, end_date)).order_by('timestamp').values('number', 'timestamp')
    for result in results:
        list_of_timestamps.append(result['timestamp'].strftime('%Y-%m-%d'))

    list_of_timestamps = np.unique(list_of_timestamps)
    return Response(list_of_timestamps)


@api_view(['GET'])
def farm_timestamps_month(request):
    user = models.User.objects.get(id = request.user.id)

    list_of_timestamps = []

    start_date = datetime.datetime.today() - datetime.timedelta(days=30)
    end_date = datetime.datetime.today()
    
    results = models.Result.objects.filter(sensor__farm = user.farm , timestamp__range = (start_date, end_date)).order_by('timestamp').values('number', 'timestamp')
    for result in results:
        list_of_timestamps.append(result['timestamp'].strftime('%Y-%m-%d'))

    list_of_timestamps = np.unique(list_of_timestamps)
    return Response(list_of_timestamps)


@api_view(['GET'])
def farm_timestamps_week(request):
    user = models.User.objects.get(id = request.user.id)

    list_of_timestamps = []
        
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
    end_date = datetime.datetime.today()
    
    results = models.Result.objects.filter(sensor__farm = user.farm , timestamp__range = (start_date, end_date)).order_by('timestamp').values('number', 'timestamp')
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
        energy_level_result = list(models.EnergyLevel.objects.filter(water_pump__id=pump_id).values_list('energy_result', flat=True))
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
        # humidity_result = list(map(int, humidity_result))
        normalized_list = []

        for reading in humidity_result:
            reading_normal = (1 - ((reading - 1700)/(2600 - 1700)) )* 100 
            normalized_list.append(round(reading_normal, 2))

        # Get the unit for the current water tank from the first result (assuming same unit for all results)
        results = models.Sensor.objects.filter(id=sensor.id)
        unit = results[0].unit if results.exists() and results[0].unit else None

        # Create a dictionary for the current water tank and append it to the data list
        data.append({
            'sensor_id': sensor_id,
            'unit': unit,
            'humidity': normalized_list,
        })

    return Response(data)


@api_view(['GET'])
def farm_general_results(request, type):
    user = models.User.objects.get(id = request.user.id)

    sensors = models.Sensor.objects.filter(farm_id=user.farm, type=type)

    # Create a list to store the data
    data = []
    for sensor in sensors:
        # Get the WaterTank ID from the water tank
        sensor_id = sensor.id

        # Get the list of water level results for the current water tank
        humidity_result = list(models.Result.objects.filter(sensor__id=sensor.id, type=type).values_list('number', flat=True))
        # humidity_result = list(map(int, humidity_result))
        

        # Get the unit for the current water tank from the first result (assuming same unit for all results)
        results = models.Sensor.objects.filter(id=sensor.id)
        unit = results[0].unit if results.exists() and results[0].unit else None

        # Create a dictionary for the current water tank and append it to the data list
        data.append({
            'sensor_id': sensor_id,
            'unit': unit,
            'number': humidity_result,
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
    water_share = models.WaterShare.objects.filter(tree__in=trees)

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
    string_results = models.StringResult.objects.filter(sensors__in = sensors)
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
    farm_id = user.farm
    weather_station = models.WeatherStation.objects.get(farm_id = farm_id)
    packet_results = models.PacketResult.objects.filter(weather_station_id = weather_station.id)
    serializer = serializers.PacketResultSerializer(packet_results, many = True)
    return Response(serializer.data)


# DATA CREATION (POST APIs)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def set_valve_state(request, valve_id, valve_state):
    try:
        valve = models.Valve.objects.get(pk=valve_id)
        # serializer = serializers.ValveSerializer(valve)
         # request.data['unit'] = sensor.unit
        # valve_state = valve_state_param
        serializer = serializers.ValveSerializer(valve, data=request.data)
        
        if serializer.is_valid():
            serializer.save(id=valve_id, state=valve_state)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except models.Valve.DoesNotExist:
        return Response({"detail": "Valve not found or does not belong to the user."}, status=404)

    
    




# DATA CREATION (POST APIs)

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from .serializers import FarmSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.home.models import Farm
from .serializers import FarmSerializer

class CreateFarmView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request):
        user = request.user

        # Check if the user already owns a farm
        if not Farm.objects.filter(owner=user.id).exists():
            data = request.data.copy()
            data['owner'] = user.id  # Add owner to the data

            serializer = FarmSerializer(data=data)
            if serializer.is_valid():
                farm = serializer.save()  # Save without owner first
                farm.owner = user.id  # Manually set the owner
                farm.save()  # Save again to update the owner field
                return Response({'message': 'Farm created successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Farm already exists, redirect to specify borders
            return Response({'message': 'Farm already exists', 'redirect_to': 'create_farm_borders'}, status=status.HTTP_302_FOUND)
        
        
class CreateFarmBordersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        farm = user.farm
        polygon = request.data.get('polygon')

        if farm and farm.polygon == "":
            if polygon:
                farm.polygon = polygon
                farm.save()
                return Response({'message': 'Farm borders updated successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'No polygon data provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Farm already has borders or no farm found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_sensor_multiple_results(request, sensor_id):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        sensor = models.Sensor.objects.get(pk=sensor_id, farm=farm)
    except models.Sensor.DoesNotExist:
        return Response({"detail": "Sensor not found or does not belong to the user."}, status=404)

    # request.data['unit'] = sensor.unit
    my_data = request.data
    loop = 0
    prev_param = []

    for param in my_data:
        # last_param = param
        if param.startswith("unit"):
            print(param)
            one_result = models.Result.objects.create(sensor=sensor, type = prev_param[0], number = prev_param[1], unit = prev_param[2])
        else:
            prev_param = [param, my_data[param], my_data["unit"+str(loop)]]
            loop+= 1

    # # serializer = serializers.ResultSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save(sensor=sensor)

    return Response(request.data, status=201)
    
    # return Response(serializer.errors, status=400)


# DATA CREATION (POST APIs)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_sensor_result(request, sensor_id):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        sensor = models.Sensor.objects.get(pk=sensor_id, farm=farm)
    except models.Sensor.DoesNotExist:
        return Response({"detail": "Sensor not found or does not belong to the user."}, status=404)

    # request.data['unit'] = sensor.unit
    my_data = request.data

    serializer = serializers.ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sensor=sensor)

        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

# DATA CREATION (POST APIs)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_packet_result(request):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        weather_station = models.WeatherStation.objects.get(farm_id = user.farm)

    except models.WeatherStation.DoesNotExist:
        return Response({"detail": "Station not found or does not belong to the user."}, status=404)

    # request.data['unit'] = sensor.unit
    my_data = request.data
    
    serializer = serializers.PacketResultSerializer(data=request.data)
    print("serializer.is_valid():: ", serializer.is_valid())
    if serializer.is_valid():
        serializer.save(weather_station=weather_station)
        # print("there")
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_watertank_result(request, watertank_id):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        watertank = models.WaterTank.objects.get(pk=watertank_id, farm = farm)
    except models.WaterTank.DoesNotExist:
        return Response({"detail": "Sensor not found or does not belong to the user."}, status=404)


    serializer = serializers.ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save( watertank = watertank )
        
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

from rest_framework import status



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_tree_result(request, tree_id):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        tree = models.Tree.objects.get(pk=tree_id, farm = farm)
    except models.Tree.DoesNotExist:
        return Response({"detail": "Sensor not found or does not belong to the user."}, status=404)


    serializer = serializers.ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(tree=tree)
        
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)





@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_valve_result(request, valve_id):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        valve = models.Valve.objects.get(pk=valve_id, farm = farm)
    except models.Valve.DoesNotExist:
        return Response({"detail": "Sensor not found or does not belong to the user."}, status=404)


    serializer = serializers.ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(valve=valve)
        
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_waterpump_energylevel(request, waterpump_id):
    try:
        user = models.User.objects.get( id = request.user.id )
        farm = models.Farm.objects.get( owner = user.id )
        waterpump = models.WaterPump.objects.get(pk=waterpump_id, farm = farm)
    except models.Sensor.DoesNotExist:
        return Response({"detail": "Sensor not found or does not belong to the user."}, status=404)


    serializer = serializers.EnergyLevelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(water_pump=waterpump)
        
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)