from django.shortcuts import render
from django.views.generic import *
from fstats.models import Statistics
from django.core import serializers


class Home(TemplateView):
    template_name = 'home.html'


class fStatsHome(TemplateView):
    template_name = 'fstats_home.html'


class HittingStatsView(ListView):
    model = Statistics
    template_name = 'hitting_stats.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_names'] = Statistics.objects.first().get_field_names()
        context['data'] = serializers.serialize('python', Statistics.objects.all())
        return context
