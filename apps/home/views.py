# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http import JsonResponse
from django import template
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np
import datetime
from .models import PacketResult
from .models import (
    Sensor,
    Valve,
    Tree,
    WaterPump,
    WaterTank,
    WeatherStation,
    Title,
    Result,
    OfflineScenario,
    Farm,
    User,
    WaterShare,
    EnergyLevel,
)


@login_required(login_url="/login/")
def index(request):
    user = User.objects.get(id=request.user.id)
    sensors = Sensor.objects.filter(farm_id=user.farm)
    weather = WeatherStation.objects.filter(farm_id=user.farm)
    valves = Valve.objects.filter(farm_id=user.farm)
    waterpumps = WaterPump.objects.filter(farm_id=user.farm)
    waterlevel = WaterTank.objects.filter(farm_id=user.farm)
    trees = Tree.objects.filter(farm_id=user.farm)

    # edit this query to get all sensors of type humidity
    start_date = (
        request.GET.get("start_date")
        if request.GET.get("start_date") != ""
        else datetime.datetime.today() - datetime.timedelta(days=30)
    )
    end_date = (
        request.GET.get("end_date")
        if request.GET.get("end_date") != ""
        else datetime.datetime.today()
    )
    if start_date is None:
        start_date = datetime.datetime.today() - datetime.timedelta(days=30)
    if end_date is None:
        end_date = datetime.datetime.today()
    humidity_results = (
        Result.objects.filter(
            sensor__type="humidity",
            sensor__farm=user.farm,
            timestamp__range=(start_date, end_date),
        )
        .order_by("timestamp")
        .values("number", "timestamp")
    )
    print(humidity_results)
    times = []
    sensor_results = []
    result_lists = [
        [result["timestamp"], result["number"]] for result in humidity_results
    ]

    for result in humidity_results:
        times.append(result["timestamp"].strftime("%Y-%m-%d"))
        sensor_results.append(result["number"])

    humidity_sensors = Sensor.objects.filter(farm_id=user.farm, type="humidity")
    list_of_humidity_results = []

    times2 = np.unique(times)
    times2 = list(times2)

    # print("start date:")
    # print(start_date)
    # print("end date:")
    # print(end_date)
    # print("times array:")
    # print(times)
    # print("times 2 array:")
    # print(times2)

    for sensor in humidity_sensors:
        # query to get number results by sensor ID
        # humidity_sensors_results = serializers.serialize("json", list(Result.objects.filter(sensor__id = sensor.id)), fields = ("number"))
        humidity_sensors_results = list(
            Result.objects.filter(sensor__id=sensor.id).values_list("number", flat=True)
        )
        list_of_humidity_results.append(humidity_sensors_results)
        # list_of_results.append(results list for each sensor)

    ###   WATER TANK   ###
    water_reading_results = Result.objects.values("number", "timestamp")
    water_time = []
    water_tank_results = []
    result_list = [
        [result["timestamp"], result["number"]] for result in water_reading_results
    ]

    for result in water_reading_results:
        water_time.append(result["timestamp"].strftime("%Y-%m-%d"))
        water_tank_results.append(result["number"])
    ###   END WATER TANK   ###

    ###   WATER SHARE   ###
    water_share_reading_results = WaterShare.objects.values("number", "timestamp")
    water_share_time = []
    water_share_results = []
    water_share_result_list = [
        [result["timestamp"], result["number"]]
        for result in water_share_reading_results
    ]

    for result in water_share_reading_results:
        water_share_time.append(result["timestamp"])
        water_share_results.append(result["number"])

    list_of_watershare_results = []

    for tree in trees:
        watershare_results = list(
            WaterShare.objects.filter(tree__id=tree.id).values_list("number", flat=True)
        )
        list_of_watershare_results.append(watershare_results)
    ###   END WATER SHARE   ###

    ###   VALVE FLOW METER   ###
    valve_flow_reading_results = Result.objects.filter(
        valve__type="flowmeter", valve__farm=user.farm
    ).values("number", "timestamp")

    valve_flow_time = []
    valve_flow_results = []
    valve_flow_result_lists = [
        [result["timestamp"], result["number"]] for result in valve_flow_reading_results
    ]

    for result in valve_flow_reading_results:
        valve_flow_time.append(result["timestamp"].strftime("%Y-%m-%d"))
        valve_flow_results.append(result["number"])

    valve_flow_meter = Valve.objects.filter(farm_id=user.farm, type="flowmeter")
    list_of_flow_meter_results = []

    for valve in valve_flow_meter:
        flow_meter_results = list(
            Result.objects.filter(valve__id=valve.id).values_list("number", flat=True)
        )
        list_of_flow_meter_results.append(flow_meter_results)
    ###   END VALVE FLOW METER   ###

    ###   ENERGY LEVEL   ###
    energy_level_reading_results = EnergyLevel.objects.values("energy_result")
    energy_level_results = []
    energy_level_result_list = [
        [result["energy_result"]] for result in energy_level_reading_results
    ]

    for result in energy_level_reading_results:
        energy_level_results.append(result["energy_result"])

    list_of_energy_level_results = []

    for pump in waterpumps:
        pump_energy_level_results = list(
            EnergyLevel.objects.filter(water_pump__id=pump.id).values_list(
                "energy_result", flat=True
            )
        )
        list_of_energy_level_results.append(pump_energy_level_results)
    ###   END ENERGY LEVEL   ###

    context = {
        "user": user,
        "results": result_lists,
        "times": times,
        "times2": times2,
        "sensor_results": sensor_results,
        "sensors": sensors,
        "trees": trees,
        "weather": weather,
        "valves": valves,
        "waterlevel": waterlevel,
        "waterpumps": waterpumps,
        "result": result_list,
        "time": water_time,
        "water_tank_results": water_tank_results,
        "water_share_results": water_share_results,
        "water_share_result_list": water_share_result_list,
        "energy_level_results": energy_level_results,
        "energy_level_result_list": energy_level_result_list,
        "valve_flow_results": valve_flow_results,
        "valve_flow_result_lists": valve_flow_result_lists,
        "humidity_sensors": humidity_sensors,
        "list_of_humidity_results": list_of_humidity_results,
        "list_of_flow_meter_results": list_of_flow_meter_results,
        "list_of_watershare_results": list_of_watershare_results,
        "list_of_energy_level_results": list_of_energy_level_results,
    }

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


def create_farm(request):
    user = User.objects.get(id=request.user.id)
    if user.farm is None:
        farm_name = request.POST.get("farm_name")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        if request.method == "POST":
            farm_object = Farm.objects.create(
                owner=request.user.id,
                farmName=farm_name,
                latitude=latitude,
                longitude=longitude,
            )
            user.farm = farm_object
            user.save()
            return redirect("create_farm_borders")
    else:
        return redirect("create_farm_borders")

    return render(request, "home/create_farm.html")


def create_farm_borders(request):
    user = User.objects.get(id=request.user.id)
    farm = Farm.objects.get(id=user.farm_id)
    if user.farm.polygon == "":
        polygon = request.POST.get("wktStringTextArea")
        if request.method == "POST":
            if polygon:
                farm.polygon = polygon

            farm.save()
            return redirect("home")
    else:
        return redirect("home")

    context = {
        "user": user,
    }
    return render(request, "home/create_farm_borders.html", context)


def weather_station(request):
    user = User.objects.get(id=request.user.id)
    weather = WeatherStation.objects.get(farm_id=user.farm)
    context = {
        "weather": weather,
    }
    html_template = loader.get_template("home/weather_station.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def offline_scenario_view(request):
    offline_scenario = OfflineScenario.objects.all()

    return render(
        request, "home/offline_scenario.html", context={"list": offline_scenario}
    )


class OfflineScenarioOperation(APIView):

    def post(self, request):
        operation = request.POST.get("operation", None)
        target_parameter = request.POST.get("target_parameter", None)
        condition = request.POST.get("condition", None)
        action = request.POST.get("action", None)
        time = request.POST.get("time", None)
        unit = request.POST.get("unit", None)
        target = request.POST.get("target", None)
        priority = request.POST.get("priority", None)

        state = request.POST.get("state", None)

        offlinescenario_id = request.POST.get("id", None)

        if operation == "edit":

            offlinescenario = OfflineScenario.objects.get(pk=offlinescenario_id)

            if target_parameter:
                offlinescenario.target_parameter = target_parameter
            if condition:
                offlinescenario.condition = condition
            if action:
                offlinescenario.action = action
            if time:
                offlinescenario.time = time
            if unit:
                offlinescenario.unit = unit
            if target:
                offlinescenario.target = target
            if priority:
                offlinescenario.priority = priority

            offlinescenario.save()

        if operation == "add":
            if (
                target_parameter
                and condition
                and action
                and time
                and unit
                and target
                and priority
            ):
                offlinescenario = OfflineScenario.objects.create(
                    target_parameter=target_parameter,
                    condition=condition,
                    action=action,
                    time=time,
                    unit=unit,
                    target=target,
                    priority=priority,
                )

        # sensors = Sensor.objects.all()
        return redirect("/assissjo-api/offline_scenario")


@login_required(login_url="/login/")
def title_view(request):
    titles = Title.objects.all()

    return render(request, "layouts/base-fullscreen.html", context={"list": titles})


@login_required(login_url="/login/")
def users_view(request):
    current_user = User.objects.get(id=request.user.id)
    farm_owner = User.objects.get(id=current_user.farm.owner)
    if request.user.id != current_user.farm.owner:
        return redirect("home")
    users = User.objects.filter(farm_id=current_user.farm)
    context = {"list": users, "farm_owner": farm_owner}

    return render(request, "home/users.html", context)


@login_required(login_url="/login/")
def create_users(request):
    msg = None
    success = False
    if request.method == "POST":
        form = CustomUserCreationForm()
        if form.is_valid():
            form.save()
            return redirect("/users")
        else:
            msg = "Form is not valid"
    else:
        form = CustomUserCreationForm()

    context = {"msg": msg, "success": success, "form": form}
    return render(request, "home/create_user.html", context)


@login_required(login_url="/login/")
def sensor_view(request):
    user = User.objects.get(id=request.user.id)
    sensors = Sensor.objects.filter(farm_id=user.farm)

    return render(request, "home/Sensor.html", context={"sensors": sensors})


def mydata_sensor(request):
    user = User.objects.get(id=request.user.id)
    result_list = list(
        Sensor.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude__exact="")
        .exclude(longitude__exact="")
        .values(
            "id",
            "location",
            "type",
            "category",
            "latitude",
            "longitude",
            "farm",
        )
        .filter(farm_id=user.farm)
    )

    return JsonResponse(result_list, safe=False)


def mydata_valve(request):
    user = User.objects.get(id=request.user.id)
    result_list = list(
        Valve.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude__exact="")
        .exclude(longitude__exact="")
        .values(
            "id",
            "location",
            "type",
            "state",
            "latitude",
            "longitude",
        )
        .filter(farm_id=user.farm)
    )

    return JsonResponse(result_list, safe=False)


def mydata_waterpump(request):
    user = User.objects.get(id=request.user.id)
    result_list = list(
        WaterPump.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude__exact="")
        .exclude(longitude__exact="")
        .values(
            "id",
            "location",
            "state",
            "latitude",
            "longitude",
            "farm",
        )
        .filter(farm_id=user.farm)
    )

    return JsonResponse(result_list, safe=False)


def mydata_watertank(request):
    user = User.objects.get(id=request.user.id)
    result_list = list(
        WaterTank.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude__exact="")
        .exclude(longitude__exact="")
        .values(
            "id",
            "water_level",
            "water_capacity",
            "location",
            "latitude",
            "longitude",
            "farm",
        )
        .filter(farm_id=user.farm)
    )

    return JsonResponse(result_list, safe=False)


def mydata_Trees(request):
    user = User.objects.get(id=request.user.id)
    result_list = list(
        Tree.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude__exact="")
        .exclude(longitude__exact="")
        .values(
            "id",
            "location",
            "type",
            "time",
            "state",
            "latitude",
            "longitude",
            "farm",
        )
        .filter(farm_id=user.farm)
    )

    return JsonResponse(result_list, safe=False)


##def mydata_weatherstation(request):

## weather_station_data = WeatherStationData.objects.all()

##context = {
##    'weather_station_data': weather_station_data,
## }

## return render(request, 'weather_station.html', context)


def mydata_weatherstation(request):
    user = User.objects.get(id=request.user.id)
    result_list = list(
        WeatherStation.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude__exact="")
        .exclude(longitude__exact="")
        .values(
            "id",
            "packet",
            "location",
            "latitude",
            "longitude",
            "farm",
        )
        .filter(farm_id=user.farm)
    )

    return JsonResponse(result_list, safe=False)


class SensorOperation(APIView):

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        operation = request.POST.get("operation", None)
        location = request.POST.get("location", None)
        type = request.POST.get("type", None)
        category = request.POST.get("category", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        sensor_id = request.POST.get("id", None)
        unit = request.POST.get("unit", None)

        if operation == "edit":
            sensor = Sensor.objects.get(pk=sensor_id)
            if location:
                sensor.location = location
            if category:
                sensor.category = category
            if type:
                sensor.type = type
            if latitude:
                sensor.latitude = latitude
            if longitude:
                sensor.longitude = longitude
            if unit:
                sensor.unit = unit
            sensor.save()

        if operation == "add":
            if location and category and type and latitude and longitude and unit:
                sensor = Sensor.objects.create(
                    location=location,
                    category=category,
                    type=type,
                    latitude=latitude,
                    longitude=longitude,
                    farm=user.farm,
                    unit=unit,
                )

        # sensors = Sensor.objects.all()
        return redirect("/assissjo-api/sensor")


@login_required(login_url="/login/")
def valve_view(request):
    user = User.objects.get(id=request.user.id)
    valves = Valve.objects.filter(farm_id=user.farm)

    return render(request, "home/valve.html", context={"valves": valves})


class ValveOperation(APIView):

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        operation = request.POST.get("operation", None)
        location = request.POST.get("location", None)
        type = request.POST.get("type", None)
        state = request.POST.get("state", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        valve_id = request.POST.get("id", None)

        if operation == "edit":
            valve = Valve.objects.get(pk=valve_id)
            if location:
                valve.location = location
            if state:
                valve.state = state
            if type:
                valve.type = type
            if latitude:
                valve.latitude = latitude
            if longitude:
                valve.longitude = longitude
            valve.save()

        if operation == "add":
            if location and state and type and latitude and longitude:
                valve = Valve.objects.create(
                    location=location,
                    state=state,
                    type=type,
                    latitude=latitude,
                    longitude=longitude,
                    farm=user.farm,
                )

        # sensors = Sensor.objects.all()
        return redirect("/assissjo-api/valve")


@login_required(login_url="/login/")
def tree_view(request):
    user = User.objects.get(id=request.user.id)
    trees = Tree.objects.filter(farm_id=user.farm)

    return render(request, "home/Tree.html", context={"list": trees})


class TreeOperation(APIView):

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        operation = request.POST.get("operation", None)
        location = request.POST.get("location", None)
        type = request.POST.get("type", None)
        state = request.POST.get("state", None)
        time = request.POST.get("time", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        tree_id = request.POST.get("id", None)

        if operation == "edit":
            tree = Tree.objects.get(pk=tree_id)
            if location:
                tree.location = location
            if state:
                tree.state = state
            if type:
                tree.type = type
            if time:
                tree.time = time
            if latitude:
                tree.latitude = latitude
            if longitude:
                tree.longitude = longitude
            tree.save()

        if operation == "add":
            if location and state and type and time and latitude and longitude:
                tree = Tree.objects.create(
                    location=location,
                    state=state,
                    type=type,
                    time=time,
                    latitude=latitude,
                    longitude=longitude,
                    farm=user.farm,
                )

        # sensors = Sensor.objects.all()
        return redirect("/assissjo-api/tree")


@login_required(login_url="/login/")
def water_pump_view(request):
    user = User.objects.get(id=request.user.id)
    water_pumps = WaterPump.objects.filter(farm_id=user.farm)

    return render(request, "home/water_pump.html", context={"water_pumps": water_pumps})


#
#
class WaterPumpOperation(APIView):

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        operation = request.POST.get("operation", None)
        location = request.POST.get("location", None)
        state = request.POST.get("state", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        waterpump_id = request.POST.get("id", None)

        if operation == "edit":
            waterpump = WaterPump.objects.get(pk=waterpump_id)
            if location:
                waterpump.location = location
            if state:
                waterpump.state = state
            if latitude:
                waterpump.latitude = latitude
            if longitude:
                waterpump.longitude = longitude
            waterpump.save()

        if operation == "add":
            if location and state and latitude and longitude:
                waterpump = WaterPump.objects.create(
                    location=location,
                    state=state,
                    latitude=latitude,
                    longitude=longitude,
                    farm=user.farm,
                )

        # sensors = Sensor.objects.all()
        return redirect("/assissjo-api/water_pump")


@login_required(login_url="/login/")
def water_tank_view(request):
    user = User.objects.get(id=request.user.id)
    water_tanks = WaterTank.objects.filter(farm_id=user.farm)

    return render(request, "home/water_tank.html", context={"water_tanks": water_tanks})


class WaterTankOperation(APIView):

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        operation = request.POST.get("operation", None)
        location = request.POST.get("location", None)
        water_level = request.POST.get("water_level", None)
        water_capacity = request.POST.get("water_capacity", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        watertank_id = request.POST.get("id", None)
        print(operation, location, water_level, watertank_id)
        if operation == "edit":
            watertank = WaterTank.objects.get(pk=watertank_id)
            if location:
                watertank.location = location
            if water_level:
                watertank.water_level = water_level
            if water_capacity:
                watertank.water_capacity = water_capacity
            if latitude:
                watertank.latitude = latitude
            if longitude:
                watertank.longitude = longitude
            watertank.save()

        if operation == "add":
            if location and water_level and water_capacity and latitude and longitude:
                water_tank = WaterTank.objects.create(
                    location=location,
                    water_level=water_level,
                    water_capacity=water_capacity,
                    latitude=latitude,
                    longitude=longitude,
                    farm=user.farm,
                )

        return redirect("/assissjo-api/water_tank")


@login_required(login_url="/login/")
def weather_station_view(request):
    user = User.objects.get(id=request.user.id)
    weather_station = WeatherStation.objects.get(farm_id=user.farm)
    return render(
        request,
        "home/weather_station.html",
        context={"weather_station": weather_station},
    )


from django.shortcuts import get_object_or_404


class WeatherStationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            weather_station = WeatherStation.objects.filter(farm=user.farm).first()

            if weather_station:
                packetresult = PacketResult.objects.filter(
                    weather_station=weather_station
                ).last()
            else:
                packetresult = None

            return render(
                request,
                "home/weather_station.html",
                context={
                    "weather_station": weather_station,
                    "packetresult": packetresult,
                },
            )

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        location = request.POST.get("location")
        packet = request.POST.get("packet")
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        new_weather_station = WeatherStation.objects.create(
            location=location,
            packet=packet,
            latitude=latitude,
            longitude=longitude,
            farm=user.farm,
        )
        WeatherStation.save()

        return HttpResponse(new_weather_station)


class WeatherStationPastView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            weather_station = WeatherStation.objects.filter(farm=user.farm).first()

            if weather_station:
                packetresult = PacketResult.objects.filter(
                    weather_station=weather_station
                ).last()
                packetresults = PacketResult.objects.filter(
                    weather_station=weather_station
                )

            else:
                packetresult = None
                packetresults = None

            return render(
                request,
                "home/weather_station_past.html",
                context={
                    "weather_station": weather_station,
                    "packetresult": packetresult,
                    "packetresults": packetresults,
                },
            )

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        location = request.POST.get("location")
        packet = request.POST.get("packet")
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        new_weather_station = WeatherStation.objects.create(
            location=location,
            packet=packet,
            latitude=latitude,
            longitude=longitude,
            farm=user.farm,
        )
        WeatherStation.save()

        return HttpResponse(new_weather_station)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin


class DisableCsrfCheck(MiddlewareMixin):
    def process_request(self, req):
        attr = "_dont_enforce_csrf_checks"
        if not getattr(req, attr, False):
            setattr(req, attr, True)


class WeatherStationAPI(APIView):
    def get_object(self, pk):
        try:
            return WeatherStation.objects.get(pk=pk)
        except WeatherStation.DoesNotExist:
            raise Http404

    def put(self, request):
        pk = request.data.get("pk", None)
        location = request.data.get("location", None)
        packet = request.data.get("packet", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        weather_station = self.get_object(pk)

        if location:
            weather_station.location = location
        if packet:
            weather_station.packet = packet
        if latitude:
            weather_station.latitude = latitude
        if longitude:
            weather_station.longitude = longitude
        weather_station.save()

        return Response(model_to_dict(weather_station))

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        location = request.data.get("location", None)
        packet = request.data.get("packet", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)

        if location and packet and latitude and longitude:
            new_weather_station = WeatherStation.objects.create(
                location=location,
                packet=packet,
                latitude=latitude,
                longitude=longitude,
                farm=user.farm,
            )
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        weather_station = self.get_object(pk)
        weather_station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteSensor(APIView):
    def delete(self, request):
        id = request.POST.get("id", None)
        sensor = Sensor.objects.get(pk=id)
        sensor.delete()
        return Response({"status": "success"})


class DeleteValve(APIView):

    def delete(self, request):
        id = request.POST.get("id", None)
        valve = Valve.objects.get(pk=id)
        valve.delete()
        return Response({"status": "success"})


class DeleteTree(APIView):

    def delete(self, request):
        id = request.POST.get("id", None)
        tree = Tree.objects.get(pk=id)
        tree.delete()
        return Response({"status": "success"})


class DeleteWaterPump(APIView):

    def delete(self, request):
        id = request.POST.get("id", None)
        water_pump = WaterPump.objects.get(pk=id)
        water_pump.delete()
        return Response({"status": "success"})


class DeleteOfflineScenario(APIView):
    def delete(self, request):
        id = request.POST.get("id", None)
        offline_scenario = OfflineScenario.objects.get(pk=id)
        offline_scenario.delete()
        return Response({"status": "success"})


class DeleteWaterTank(APIView):
    def delete(self, request):
        id = request.POST.get("id", None)
        water_tank = WaterTank.objects.get(pk=id)
        water_tank.delete()
        return Response({"status": "success"})


class DeleteWeatherstation(APIView):
    def delete(self, request):
        id = request.POST.get("id", None)
        Weather_Station = WeatherStation.objects.get(pk=id)
        print(Weather_Station)
        Weather_Station.delete()
        return Response({"status": "success"})


class WeatherStationOperation(APIView):
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        operation = request.POST.get("operation", None)
        location = request.POST.get("location", None)
        latitude = request.POST.get("latitude", None)
        longitude = request.POST.get("longitude", None)
        WeatherStation_id = request.POST.get("id", None)

        if operation == "edit":
            weather_station = WeatherStation.objects.get(pk=WeatherStation_id)

            if location:
                weather_station.location = location
            if latitude:
                weather_station.latitude = latitude
            if longitude:
                weather_station.longitude = longitude
            weather_station.save()

        if operation == "add":
            if location and latitude and longitude:
                weather_station = WeatherStation.objects.create(
                    location=location,
                    latitude=latitude,
                    longitude=longitude,
                    farm=user.farm,
                )

        return redirect("/assissjo-api/weather_station")


class UserOperation(APIView):
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        operation = "add"
        # operation = request.POST.get('operation', None)
        # user_id = request.POST.get('id', None)

        # if operation == 'edit':
        #     sensor = Sensor.objects.get(pk=sensor_id)
        #     if location:
        #         sensor.location = location
        #     if category:
        #         sensor.category = category
        #     if type:
        #         sensor.type = type
        #     if latitude:
        #         sensor.latitude = latitude
        #     if longitude:
        #         sensor.longitude = longitude
        #     sensor.save()

        if operation == "add":
            if username and email and password:
                varuser = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    farm=user.farm,
                )
                varuser.save()
        return redirect("/assissjo-api/users")


## def index(request):

## user = User.objects.get(id=request.user.id)
## packetresult = PacketResult.objects.last()
##return render(request, 'home\index.html', context={'packetresult': packetresult})


def index(request):
    if request.user.is_authenticated:
        user = request.user
        farm = user.farm
        packetresult = PacketResult.objects.filter(weather_station__farm=farm).last()
        sensors = Sensor.objects.filter(farm=farm)
        return render(
            request,
            "home/index.html",
            context={"packetresult": packetresult, "sensors": sensors},
        )
    else:
        login_url = reverse("login")
        return redirect(login_url)
