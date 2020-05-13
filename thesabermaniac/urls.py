from django.contrib import admin
from django.urls import path, include
from fstats.views import Home, HittingStatsView

urlpatterns = [
    path('', Home.as_view()),
    path('admin/', admin.site.urls),
    path('fstats/', include('fstats.urls')),
    path('hitting/', HittingStatsView.as_view()),
]
