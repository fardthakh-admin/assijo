# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http import JsonResponse
from django.template.context_processors import request
from rest_framework import generics
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import routers,  viewsets

from .models import Sensor, Valve, Tree, WaterPump, WaterTank, WeatherStation, Title, Result, OfflineScenario



@login_required(login_url="/login/")
def index(request):
    results = Result.objects.filter(sensor__type='humidity').values('number', 'timestamp')
    times = []
    sensor_results = []
    result_lists = [[result['timestamp'], result['number']] for result in results]

    wresults = Result.objects.values('number', 'timestamp')
    time = []
    water_tank_results = []
    result_list = [[result['timestamp'], result['number']] for result in results]

    for result in results:
        times.append(result['timestamp'].strftime('%Y-%m-%d'))
        sensor_results.append(result['number'])

    for result in wresults:
        time.append(result['timestamp'].strftime('%Y-%m-%d'))
        water_tank_results.append(result['number'])

    sensors = Sensor.objects.all()
    weather = WeatherStation.objects.last()
    valve = Valve.objects.last()
    waterpump = WaterPump.objects.last()
    waterlevel = WaterTank.objects.last()

    trees = Tree.objects.all()
    context = {'results': result_lists,
               'times': times,
               'sensor_results': sensor_results,
               'sensors': sensors,
               'trees': trees,
               'weather': weather,
               'valve': valve,
               'waterlevel': waterlevel,
               'waterpump': waterpump,
               'result': result_list,
               'time': time,
               'water_tank_results': water_tank_results,
               }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def weather_station(request):
    weather = WeatherStation.objects.last()
    print("I am called")
    print(weather)
    context = {
               'weather': weather,
               }
    html_template = loader.get_template('home/weather_station.html')
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def offline_scenario_view(request):
    offline_scenario = OfflineScenario.objects.all()

    return render(request, 'home/offline_scenario.html', context={'list': offline_scenario})


class OfflineScenarioOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        target_parameter = request.POST.get('target_parameter', None)
        condition = request.POST.get('condition', None)
        action = request.POST.get('action', None)
        time = request.POST.get('time', None)
        unit = request.POST.get('unit', None)
        target = request.POST.get('target', None)
        priority = request.POST.get('priority', None)

        state = request.POST.get('state', None)

        offlinescenario_id = request.POST.get('id', None)

        if operation == 'edit':

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

        if operation == 'add':
            if target_parameter and condition and action and time and unit and target and priority:
                offlinescenario = OfflineScenario.objects.create(target_parameter=target_parameter, condition=condition,
                                                                 action=action, time=time, unit=unit, target=target,
                                                                 priority=priority)

        # sensors = Sensor.objects.all()
        return redirect('/offline_scenario')


@login_required(login_url="/login/")
def title_view(request):
    titles = Title.objects.all()

    return render(request, 'layouts/base-fullscreen.html', context={'list': titles})


@login_required(login_url="/login/")
def sensor_view(request):
    sensors = Sensor.objects.all()

    return render(request, 'home/Sensor.html', context={'list': sensors})

def mydata_sensor(request):
    result_list = list(Sensor.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'location',
                               'type',
                               'category',
                               'latitude',
                               'longitude',
                               ))

    return JsonResponse(result_list, safe=False)

def mydata_valve(request):
    result_list = list(Valve.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'location',
                               'type',
                               'state',
                               'latitude',
                               'longitude',
                               ))

    return JsonResponse(result_list, safe=False)

def mydata_waterpump(request):
    result_list = list(WaterPump.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'location',
                               'state',
                               'latitude',
                               'longitude',
                               ))

    return JsonResponse(result_list, safe=False)

def mydata_watertank(request):
    result_list = list(WaterTank.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'water_level',
                               'water_capacity',
                               'location',
                               'latitude',
                               'longitude',
                               ))

    return JsonResponse(result_list, safe=False)

def mydata_Trees(request):
    result_list = list(Tree.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'location',
                               'type',
                               'time',
                               'state',
                               'latitude',
                               'longitude',
                               ))

    return JsonResponse(result_list, safe=False)

def mydata_weatherstation(request):
    result_list = list(WeatherStation.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'packet',
                               'location',
                               'latitude',
                               'longitude',
                               ))

    return JsonResponse(result_list, safe=False)


class SensorOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        type = request.POST.get('type', None)
        category = request.POST.get('category', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        sensor_id = request.POST.get('id', None)

        if operation == 'edit':
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
            sensor.save()

        if operation == 'add':
            if location and category and type and latitude and longitude:
                sensor = Sensor.objects.create(location=location, category=category, type=type, latitude=latitude, longitude=longitude)

        # sensors = Sensor.objects.all()
        return redirect('/sensor')


@login_required(login_url="/login/")
def valve_view(request):
    valves = Valve.objects.all()

    return render(request, 'home/valve.html', context={'list': valves})


class ValveOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        type = request.POST.get('type', None)
        state = request.POST.get('state', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        valve_id = request.POST.get('id', None)

        if operation == 'edit':
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

        if operation == 'add':
            if location and state and type and latitude and longitude:
                valve = Valve.objects.create(location=location, state=state, type=type, latitude=latitude, longitude=longitude)

        # sensors = Sensor.objects.all()
        return redirect('/valve')


@login_required(login_url="/login/")
def tree_view(request):
    trees = Tree.objects.all()

    return render(request, 'home/Tree.html', context={'list': trees})


class TreeOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        type = request.POST.get('type', None)
        state = request.POST.get('state', None)
        time = request.POST.get('time', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        tree_id = request.POST.get('id', None)

        if operation == 'edit':
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

        if operation == 'add':
            if location and state and type and time and latitude and longitude:
                tree = Tree.objects.create(location=location, state=state, type=type, time=time, latitude=latitude, longitude=longitude)

        # sensors = Sensor.objects.all()
        return redirect('/tree')


@login_required(login_url="/login/")
def water_pump_view(request):
    water_pumps = WaterPump.objects.all()

    return render(request, 'home/water_pump.html', context={'list': water_pumps})


#
#
class WaterPumpOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        state = request.POST.get('state', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        waterpump_id = request.POST.get('id', None)

        if operation == 'edit':
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

        if operation == 'add':
            if location and state and latitude and longitude:
                waterpump = WaterPump.objects.create(location=location, state=state, latitude=latitude, longitude=longitude)

        # sensors = Sensor.objects.all()
        return redirect('/water_pump')


@login_required(login_url="/login/")
def water_tank_view(request):
    water_tanks = WaterTank.objects.all()

    return render(request, 'home/water_tank.html', context={'list': water_tanks})


class WaterTankOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        water_level = request.POST.get('water_level', None)
        water_capacity = request.POST.get('water_capacity', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        watertank_id = request.POST.get('id', None)
        print(operation, location, water_level, watertank_id)
        if operation == 'edit':
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

        if operation == 'add':
            if location and water_level and water_capacity and latitude and longitude:
                water_tank = WaterTank.objects.create(location=location, water_level=water_level, water_capacity=water_capacity, latitude=latitude,longitude=longitude)

        return redirect('/water_tank')


@login_required(login_url="/login/")
def weather_station_view(request):
    weather_station = WeatherStation.objects.all()
    weather = WeatherStation.objects.last()
    print("I am called")
    print(weather)
    context = {
        'weather': weather,
    }
    return render(request, 'home/weather_station.html', context={'list': weather_station})


class WeatherStationView(View):

    def get(self, request):
        weather_station = WeatherStation.objects.all()
        weather = WeatherStation.objects.last()
        print("I am called")
        print(weather)

        return render(request, 'home/weather_station.html', context={'list': weather_station , 'weather': weather})

    def post(self, request):
        location = request.POST.get('location')
        packet = request.POST.get('packet')
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        new_weather_station = WeatherStation.objects.create(location=location, packet=packet, latitude=latitude, longitude=longitude)

        return HttpResponse(new_weather_station)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin


class DisableCsrfCheck(MiddlewareMixin):

    def process_request(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)


class WeatherStationAPI(APIView):

    def get_object(self, pk):
        try:
            return WeatherStation.objects.get(pk=pk)
        except WeatherStation.DoesNotExist:
            raise Http404

    def put(self, request):
        pk = request.data.get('pk', None)
        location = request.data.get('location', None)
        packet = request.data.get('packet', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
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
        location = request.data.get('location', None)
        packet = request.data.get('packet', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)

        if location and packet and latitude and longitude:
            new_weather_station = WeatherStation.objects.create(location=location, packet=packet, latitude=latitude,longitude=longitude)
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        weather_station = self.get_object(pk)
        weather_station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteSensor(APIView):

    def delete(self, request):
        id = request.POST.get('id', None)
        sensor = Sensor.objects.get(pk=id)
        sensor.delete()
        return Response({'status': 'sucsses'})


class DeleteValve(APIView):

    def delete(self, request):
        id = request.POST.get('id', None)
        valve = Valve.objects.get(pk=id)
        valve.delete()
        return Response({'status': 'sucsses'})


class DeleteTree(APIView):

    def delete(self, request):
        id = request.POST.get('id', None)
        tree = Tree.objects.get(pk=id)
        tree.delete()
        return Response({'status': 'sucsses'})


class DeleteWaterPump(APIView):

    def delete(self, request):
        id = request.POST.get('id', None)
        water_pump = WaterPump.objects.get(pk=id)
        water_pump.delete()
        return Response({'status': 'sucsses'})


class DeleteOfflineScenario(APIView):

    def delete(self, request):
        id = request.POST.get('id', None)
        offline_scenario = OfflineScenario.objects.get(pk=id)
        offline_scenario.delete()
        return Response({'status': 'sucsses'})


class DeleteWaterTank(APIView):

    def delete(self, request):
        id = request.POST.get('id', None)
        water_tank = WaterTank.objects.get(pk=id)
        water_tank.delete()
        return Response({'status': 'sucsses'})

class DeleteWeatherstation(APIView):
    def delete(self, request):
        id = request.POST.get('id', None)
        Weather_Station = WeatherStation.objects.get(pk=id)
        print(Weather_Station)
        Weather_Station.delete()
        return Response({'status': 'sucsses'})

class WeatherStationOperation(APIView):
    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        WeatherStation_id = request.POST.get('id', None)

        if operation == 'edit':
            weather_station = WeatherStation.objects.get(pk=WeatherStation_id)

            if location:
                weather_station.location = location
            if latitude:
                weather_station.latitude = latitude
            if longitude:
                weather_station.longitude = longitude
            weather_station.save()

        if operation == 'add':
            if location and latitude and longitude:
                weather_station = WeatherStation.objects.create(location=location, latitude=latitude,longitude=longitude)

        return redirect('/weather_station')
