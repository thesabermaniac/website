from django.urls import path

from stats.views import HittingStatsView, PitchingStatsView
urlpatterns = [
    path('hitting/', HittingStatsView.as_view()),
    path('pitching/', PitchingStatsView.as_view())
]
