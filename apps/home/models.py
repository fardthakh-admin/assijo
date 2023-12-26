# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Farm(models.Model):
    '''
    a farm can have many users
    a farm can have many trees
    a farm can have many sensors
    a farm can have many valves
    a farm can have many watertanks
    a farm can have many waterpumps
    a farm can have many offline scenarios
    a farm can have one weather station
    a farm can have one gateway
    a farm has longitude and latitude
    '''

    farmName = models.CharField(max_length = 200, default = "MyFarm")
    owner = models.IntegerField()
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    polygon = models.TextField(default="", blank=True)
    def __str__(self):
        return self.farmName

class User(AbstractUser):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.username

class Title(models.Model):
    title = models.CharField(max_length=60)
    def __str__(self):
        return self.title


class Sensor(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    unit = models.CharField(max_length=200, blank = True, null = True , default="Sensor Default Unit")
    # def __str__(self):
    #     return "%s %s" % (self.id, self.type)


class Valve(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)

    def __int__(self):
         return self.id


class WaterTank(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
    water_level = models.FloatField(default = 0.0)
    water_capacity = models.FloatField(default = 100.0)
    location = models.CharField(max_length=40, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    # def __str__(self):
    #     return "%s %s" % (self.water_level, self.location)


class WaterPump(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
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

    def __str__(self):
        return "%s %s" % (self.energy_result, self.water_pump)


class Result(models.Model):
    number = models.IntegerField(default=0)
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
            return 'no sensors'
    def save(self, *args, **kwargs):
        sensor = Sensor.objects.get(pk=self.sensor.id)
        self.unit = sensor.unit
        super().save(*args, **kwargs)  # Call the "real" save() method.

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
            return 'no sensors'


class OfflineScenario(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
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
    farm = models.OneToOneField(Farm, null=True, on_delete=models.SET_NULL)
    list_filter = ()
    location = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    list_filter = ('location', 'location')


# def __str__(self):
# return "%s %s" % (self.location, self.state)


class Tree(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True)
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
    takes the result as a foreign key from the packet result
    """
    farm = models.OneToOneField(Farm, null=True, on_delete=models.SET_NULL)
    packet = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)

    BattV_MinUnit	      = models.CharField(max_length=100, blank=True, null=True)
    BattV_AvgUnit	      = models.CharField(max_length=30, blank=True, null=True)
    PTemp_C_AvgUnit	      = models.CharField(max_length=30, blank=True, null=True)
    BP_mmHg_AvgUnit	      = models.CharField(max_length=30, blank=True, null=True)
    Rain_mm_TotUnit	      = models.CharField(max_length=30, blank=True, null=True)
    AirTC_AvgUnit	      = models.CharField(max_length=30, blank=True, null=True)
    AirTC_MaxUnit	      = models.CharField(max_length=30, blank=True, null=True)
    AirTC_TMxUnit	      = models.CharField(max_length=30, blank=True, null=True)
    AirTC_MinUnit	      = models.CharField(max_length=30, blank=True, null=True)
    AirTC_TMnUnit	      = models.CharField(max_length=30, blank=True, null=True)
    RHUnit	              = models.CharField(max_length=30, blank=True, null=True)
    SlrkW_AvgUnit	      = models.CharField(max_length=30, blank=True, null=True)
    SlrMJ_TotUnit	      = models.CharField(max_length=30, blank=True, null=True)
    Visibility_m_AvgUnit  = models.CharField(max_length=30, blank=True, null=True)
    wind_speed_AVGUnit	  = models.CharField(max_length=30, blank=True, null=True)
    
  
# def __str__(self):
#   return "%s %s" % (self.packet, self.location)

#here
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

    # def save(self, *args, **kwargs):
    #     # weather_station = WeatherStation.objects.get(pk=self.weather_station.id)
    #     # self.unit = sensor.unit
    #     super().save(*args, **kwargs)