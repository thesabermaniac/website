from django.urls import path

from stats.views import HittingStatsView
urlpatterns = [
    path('hitting/', HittingStatsView.as_view()),
]
