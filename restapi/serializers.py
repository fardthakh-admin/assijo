from rest_framework import serializers
from apps.home import models
from apps.home.models import Farm
class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Farm
        fields = '__all__'
       
        # extra_kwargs = {'owner': {'read_only': True}}

    def create(self, validated_data):
        instance = Farm.objects.create(**validated_data)
        return instance

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
    farm_name = serializers.SerializerMethodField()
    class Meta:
        model = models.Sensor
        fields = '__all__'
    def get_farm_name(self, obj):
        return obj.farm.farmName if obj.farm else None

class ValveSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Valve
        fields = '__all__'
    def get_farm_name(self, obj):
        return obj.farm.farmName if obj.farm else None
    
class WaterTankSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterTank
        fields = '__all__'
    def get_farm_name(self, obj):
        return obj.farm.farmName if obj.farm else None

class WaterPumpSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = models.WaterPump
        fields = '__all__'
    def get_farm_name(self, obj):
        return obj.farm.farmName if obj.farm else None
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
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Tree
        fields = '__all__'
    def get_farm_name(self, obj):
        return obj.farm.farmName if obj.farm else None
class WaterShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WaterShare
        fields = '__all__'

class WeatherStationSerializer(serializers.ModelSerializer):
    farm_name = serializers.SerializerMethodField()

    class Meta:
        model = models.WeatherStation
        fields = '__all__'
    def get_farm_name(self, obj):
        return obj.farm.farmName if obj.farm else None
class PacketResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PacketResult
        fields = '__all__'