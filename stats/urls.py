from django.urls import path

from stats.views import StatsListView
from stats.models import HittingStatistics, PitchingStatistics

urlpatterns = [
    path('hitting/', StatsListView.as_view(model=HittingStatistics)),
    path('pitching/', StatsListView.as_view(model=PitchingStatistics))
]
