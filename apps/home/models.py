# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Title(models.Model):
    title = models.CharField(max_length=60)


class Sensor(models.Model):
    location = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    # def __str__(self):
    #     return "%s %s" % (self.id, self.type)


class Valve(models.Model):
    location = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    #
    # def __str__(self):
    #     return "%s %s" % (self.id, self.type, self.location)


class WaterTank(models.Model):
    water_level = models.CharField(max_length=40)
    location = models.CharField(max_length=40)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    # def __str__(self):
    #     return "%s %s" % (self.water_level, self.location)


class WaterPump(models.Model):
    location = models.CharField(max_length=40)
    state = models.CharField(max_length=30)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    # def __str__(self):
    #     return "%s %s" % (self.state, self.location)


class EnergyLevel(models.Model):
    energy_result = models.CharField(max_length=40)
    water_pump = models.ForeignKey(WaterPump, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="water_pump")

    # def __str__(self):
    #     return "%s %s" % (self.energy_result, self.water_pump)


class Result(models.Model):
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, blank=True, null=True, related_name="number_results")
    valve = models.ForeignKey(Valve, on_delete=models.SET_NULL, blank=True, null=True, related_name="vnumber_results")
    water_tank = models.ForeignKey(WaterTank, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="watertank")
    water_pump = models.ForeignKey(WaterPump, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="waterpump")
    energy_level = models.ForeignKey(EnergyLevel, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name="energylevel")

    def __str__(self):
        try:
            return "sensor {}".format(str(self.sensor.pk))
        except:
            return 'no sesnsors'


class StringResult(models.Model):
    string_result = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    sensors = models.ForeignKey(Sensor, on_delete=models.CASCADE, blank=True, null=True, related_name="STRINGRESULT")
    valves = models.ForeignKey(Valve, on_delete=models.SET_NULL, blank=True, null=True, related_name="vSTRINGRESULT")
    water_tanks = models.ForeignKey(WaterTank, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name="swatertank")

    def __str__(self):
        try:
            return str(self.sensors.pk)
        except:
            return 'no sesnsors'


class OfflineScenario(models.Model):
    target_parameter = models.CharField(max_length=100)
    condition = models.CharField(max_length=40)
    action = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    unit = models.CharField(max_length=30)
    target = models.CharField(max_length=100)
    priority = models.CharField(max_length=30)


# def __str__(self):
#   return "%s %s" % (self.target, self.name, self.priority, self.action)


class Gateway(models.Model):
    list_filter = ()
    location = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    list_filter = ('location', 'location')


# def __str__(self):
# return "%s %s" % (self.location, self.state)


class Tree(models.Model):
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)

# def __str__(self):
#   return "%s %s" % (self.type, self.state)


class WaterShare(models.Model):
    number = models.IntegerField(default=0)
    unit = models.CharField(max_length=100)
    time = models.CharField(max_length=30)
    timestamp = models.CharField(max_length=30)
    tree = models.ForeignKey(Tree, on_delete=models.SET_NULL, blank=True, null=True, related_name="water_share")


# def __str__(self):
#   return "%s %s" % (self.number, self.timestamp)


class WeatherStation(models.Model):
    """
    takes the result as a forgin key from the packet result
    """
    packet = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)

# def __str__(self):
#   return "%s %s" % (self.packet, self.location)


class PacketResult(models.Model):
    temperature = models.CharField(max_length=100)
    humidity = models.CharField(max_length=30)
    rainfall = models.CharField(max_length=30)
    wind_speed = models.CharField(max_length=30)
    timestamp = models.CharField(max_length=30)
    direction = models.CharField(max_length=30)
    visibility = models.CharField(max_length=30)
    solar_radiation = models.CharField(max_length=30)
    weather_station = models.ForeignKey(WeatherStation, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name="weather_station")
