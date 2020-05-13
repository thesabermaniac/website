from django.contrib import admin
from .models import Player, Statistics


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    fields = ('fName', 'lName', 'position')
    list_display = ('fName', 'lName', 'position')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year')
