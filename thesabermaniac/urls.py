from django.contrib import admin
from django.urls import path, include
from stats.views import Home, StatsListView, BigBoardView, TradeAnalyzer

urlpatterns = [
    path('', Home.as_view()),
    path('admin/', admin.site.urls),
    path('stats/', include('stats.urls')),
    path('bigboard/', BigBoardView.as_view()),
    path('trade-analyzer/', TradeAnalyzer.as_view())
]
