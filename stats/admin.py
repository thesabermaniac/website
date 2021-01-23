from django.contrib import admin
from .models import Player, HittingStatistics, PitchingStatistics


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    fields = ('fName', 'lName', 'position')
    list_display = ('fName', 'lName', 'position')


@admin.register(HittingStatistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'is_projection')
    search_fields = ('player__lName', 'player__fName', 'year')


@admin.register(PitchingStatistics)
class PitchingStatisticsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year')
    ordering = ('player__lName', 'player__fName')
    search_fields = ('player__lName', 'player__fName', 'year')
