from django.contrib import admin
from django.urls import path, include
from stats.views import Home, HittingStatsView, fStatsHome

urlpatterns = [
    path('', Home.as_view()),
    path('admin/', admin.site.urls),
    path('stats/', include('stats.urls')),
    path('fstats/', fStatsHome.as_view()),
]
