from django.urls import path

from . import views

urlpatterns = [
    path('', views.fStatsHome.as_view(), name='index'),
]
