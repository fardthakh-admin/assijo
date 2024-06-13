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
from .models import User
from .models import Farm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import home_user


# class ResultInline(admin.ModelAdmin):
#     model = Result


# Register your models here.
class PacketResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PacketResult._meta.get_fields()]
    # fields = [field.name for field in Result._meta.get_fields()]

    list_filter = ["weather_station"]
    model = PacketResult


class ResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Result._meta.get_fields()]
    # fields = [field.name for field in Result._meta.get_fields()]

    list_filter = ["unit", "sensor"]
    model = Result


# Register your models here.
class ResultInline(admin.StackedInline):
    model = Result


class EnergyLevelInline(admin.StackedInline):
    model = EnergyLevel
    inlines = [ResultInline]


class WaterShareInline(admin.StackedInline):
    model = WaterShare


class TreeAdmin(admin.ModelAdmin):
    list_display = ("location", "type", "time", "state", "latitude", "longitude")
    inlines = [WaterShareInline]


class StringResultInline(admin.StackedInline):
    model = StringResult


class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "type", "category", "latitude", "longitude")
    # inlines = [ResultInline, StringResultInline]


class WaterPumpAdmin(admin.ModelAdmin):
    list_display = ("location", "state", "latitude", "longitude")
    inlines = [ResultInline, EnergyLevelInline]


class WaterTankAdmin(admin.ModelAdmin):
    list_display = (
        "location",
        "water_level",
        "water_capacity",
        "latitude",
        "longitude",
    )
    inlines = [ResultInline, StringResultInline]


class ValveInAdmin(admin.ModelAdmin):
    list_display = ("location", "type", "state", "latitude", "longitude")
    inlines = [ResultInline, StringResultInline]


class PacketResultInline(admin.StackedInline):
    model = PacketResult


class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ("location", "packet", "latitude", "longitude")
    inlines = [PacketResultInline]


class TitleStationAdmin(admin.ModelAdmin):
    list_display = ("title",)


class CustomUserAdmin(UserAdmin):
    model = home_user


admin.site.register(home_user, CustomUserAdmin)


admin.site.register(Sensor, SensorAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(PacketResult, PacketResultAdmin)
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
# admin.site.register(PacketResult)
admin.site.register(Title)
admin.site.register(User)
admin.site.register(Farm)
