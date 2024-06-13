from rest_framework import serializers
from apps.home import models

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Farm
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Title
        fields = '__all__'


class TimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ['timestamp']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sensor
        fields = '__all__'

class ValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Valve
        fields = '__all__'
    
class WaterTankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterTank
        fields = '__all__'

class WaterPumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterPump
        fields = '__all__'

class EnergyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnergyLevel
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = '__all__'

class StringResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StringResult
        fields = '__all__'

class OfflineScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OfflineScenario
        fields = '__all__'

class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gateway
        fields = '__all__'

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tree
        fields = '__all__'

class WaterShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterShare
        fields = '__all__'

class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeatherStation
        fields = '__all__'

class PacketResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PacketResult
        fields = '__all__'