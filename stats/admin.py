from django.contrib import admin
from .models import Player, HittingStatistics, PitchingStatistics


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    fields = ('name', 'position')
    list_display = ('name', 'position')
    search_fields = ['name']


@admin.register(HittingStatistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'is_projection', 'projection_system')
    search_fields = ('player__name', 'year')


@admin.register(PitchingStatistics)
class PitchingStatisticsAdmin(admin.ModelAdmin):
    list_display = ('player', 'year', 'is_projection', 'projection_system')
    ordering = ['player__name']
    search_fields = ('player__name', 'year')
