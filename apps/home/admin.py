from django.contrib import admin
from .models import Sensor
from .models import Valve
from .models import WaterTank
from .models import WaterPump
from .models import EnergyLevel
from .models import Result
from .models import StringResult
from .models import OfflineScenario
from .models import Gateway
from .models import Tree
from .models import WaterShare
from .models import WeatherStation
from .models import PacketResult
from .models import Title
from django.contrib.auth.models import Group


# class ResultInline(admin.ModelAdmin):
#     model = Result


# Register your models here.
class ResultInline(admin.StackedInline):
    model = Result


class EnergyLevelInline(admin.StackedInline):
    model = EnergyLevel
    inlines = [ResultInline]


class WaterShareInline(admin.StackedInline):
    model = WaterShare


class TreeAdmin(admin.ModelAdmin):
    list_display = ('location', 'type', 'time', 'state', 'latitude', 'longitude')
    inlines = [WaterShareInline]


class StringResultInline(admin.StackedInline):
    model = StringResult


class SensorAdmin(admin.ModelAdmin):
    list_display = ('location', 'type', 'category', 'latitude', 'longitude')
    inlines = [ResultInline, StringResultInline]


class WaterPumpAdmin(admin.ModelAdmin):
    list_display = ('location', 'state', 'latitude', 'longitude')
    inlines = [ResultInline, EnergyLevelInline]


class WaterTankAdmin(admin.ModelAdmin):
    list_display = ('location', 'water_level', 'water_capacity', 'latitude', 'longitude')
    inlines = [ResultInline, StringResultInline]


class ValveInAdmin(admin.ModelAdmin):
    list_display = ('location', 'type', 'state', 'latitude', 'longitude')
    inlines = [ResultInline, StringResultInline]


class PacketResultInline(admin.StackedInline):
    model = PacketResult


class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ('location', 'packet', 'latitude', 'longitude')
    inlines = [PacketResultInline]


class TitleStationAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Sensor, SensorAdmin)
admin.site.register(Result)
admin.site.register(Valve, ValveInAdmin)
admin.site.register(WaterTank, WaterTankAdmin)
admin.site.register(WaterPump, WaterPumpAdmin)
admin.site.register(EnergyLevel)
admin.site.register(StringResult)
admin.site.register(OfflineScenario)
admin.site.register(Gateway)
admin.site.register(Tree, TreeAdmin)
admin.site.register(WaterShare)
admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(PacketResult)
admin.site.register(Title)
