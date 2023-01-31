# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Sensor, Valve, Tree, WaterPump, WaterTank, WeatherStation


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
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
def sensor_view(request):
    sensors = Sensor.objects.all()

    return render(request, 'home/Sensor.html', context={'list': sensors})


class SensorOperation(APIView):

    def post(self, request):
        operation = request.POST.get('operation', None)
        location = request.POST.get('location', None)
        type = request.POST.get('type', None)
        category = request.POST.get('category', None)
        sensor_id = request.POST.get('id',None)

        if operation == 'edit':
            sensor = Sensor.objects.get(pk=sensor_id)
            if location:
                sensor.location = location
            if category:
                sensor.category = category
            if type:
                sensor.type = type

            sensor.save()

        if operation == 'add':
            if location and category and type:
                sensor = Sensor.objects.create(location=location,category=category,type=type)

        sensors = Sensor.objects.all()
        return render(request, 'home/Sensor.html', context={'list': sensors})


@login_required(login_url="/login/")
def valve_view(request):
    valves = Valve.objects.all()

    return render(request, 'home/valve.html', context={'list': valves})


@login_required(login_url="/login/")
def tree_view(request):
    trees = Tree.objects.all()

    return render(request, 'home/Tree.html', context={'list': trees})


@login_required(login_url="/login/")
def water_pump_view(request):
    water_pumps = WaterPump.objects.all()

    return render(request, 'home/water_pump.html', context={'list': water_pumps})


#
#
@login_required(login_url="/login/")
def water_tank_view(request):
    water_tanks = WaterTank.objects.all()

    return render(request, 'home/water_tank.html', context={'list': water_tanks})


@login_required(login_url="/login/")
def weather_station_view(request):
    weather_station = WeatherStation.objects.all()

    return render(request, 'home/weather_station.html', context={'list': weather_station})


class WeatherStationView(View):

    def get(self, request):
        weather_station = WeatherStation.objects.all()

        return render(request, 'home/weather_station.html', context={'list': weather_station})

    def post(self, request):
        location = request.POST.get('location')
        packet = request.POST.get('packet')

        new_weather_station = WeatherStation.objects.create(location=location, packet=packet)

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

        weather_station = self.get_object(pk)

        if location:
            weather_station.location = location
        if packet:
            weather_station.packet = packet
        weather_station.save()

        return Response(model_to_dict(weather_station))

    def post(self, request):
        location = request.data.get('location', None)
        packet = request.data.get('packet', None)

        if location and packet:
            new_weather_station = WeatherStation.objects.create(location=location, packet=packet)
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
