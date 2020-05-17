from django.shortcuts import render
from django.views.generic import *
from stats.models import HittingStatistics, Player
from django.core import serializers
from django.db.models import *


class Home(TemplateView):
    template_name = 'home.html'


class fStatsHome(TemplateView):
    model = HittingStatistics
    template_name = 'fstats_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stat_list = ['player', 'year']
        stat_list.extend(self.request.GET.getlist('include'))
        for stat in self.request.GET.getlist('include'):
            stat_list.append("f" + stat)
        stat_list.append("fTotal")
        context['field_names'] = HittingStatistics.objects.first().get_field_names()
        context['included_field_names'] = stat_list if self.request.GET.get('include') else HittingStatistics.objects.first().get_field_names()
        context['object_list'] = HittingStatistics.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('include'):
            stats_list = request.GET.getlist('include')
            for stat in stats_list:
                fStat = "f" + stat
                average = HittingStatistics.objects.all().aggregate(Avg(stat))[stat + "__avg"]
                max = HittingStatistics.objects.all().aggregate(Max(stat))[stat + "__max"]
                control = 100/((max - average)/average * 100)
                for row in HittingStatistics.objects.all():
                    if getattr(row, fStat) is None:
                        increase = getattr(row, stat) - average
                        percent_increase = increase/average * 100
                        setattr(row, fStat, int(100 + (percent_increase * control)))
                        row.save()
                        if stat == stats_list[-1]:
                            fTotal = 0
                            for score in stats_list:
                                fTotal += getattr(row, "f" + score)
                            row.fTotal = int(fTotal)/len(stats_list)
                            row.save()
        return render(request, 'fstats_home.html', context=self.get_context_data())


class HittingStatsView(ListView):
    model = HittingStatistics
    template_name = 'hitting_stats.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_names'] = HittingStatistics.objects.first().get_field_names_and_values()
        context['data'] = serializers.serialize('python', HittingStatistics.objects.all())
        return context
