from django.shortcuts import render
from django.views.generic import *
from stats.models import HittingStatistics, Player, PitchingStatistics
from django.core import serializers
from django.db.models import *


class Home(TemplateView):
    template_name = 'home.html'


class fStatsHome(TemplateView):
    model = HittingStatistics
    template_name = 'fstats_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = HittingStatistics.objects.all().order_by('fTotal')

        stat_list = ['player', 'year']
        stat_list.extend(self.request.GET.getlist('include'))
        for stat in self.request.GET.getlist('include'):
            stat_list.append("f" + stat)
        stat_list.append("fTotal")

        if self.request.GET.get('year'):
            object_list = object_list.filter(year=self.request.GET.get('year'))

        if self.request.GET.get('min_pa'):
            object_list = object_list.filter(PA__gte=self.request.GET.get('min_pa'))

        context['field_names'] = HittingStatistics.objects.first().get_field_names()
        context['included_field_names'] = stat_list if self.request.GET.get('include') else HittingStatistics.objects.first().get_field_names()
        context['object_list'] = object_list.order_by('fTotal')
        context['year_list'] = HittingStatistics.objects.order_by().values_list('year', flat=True).distinct()
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


class HittingStatsView(TemplateView):
    model = HittingStatistics
    template_name = 'hitting_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = HittingStatistics.objects.filter(PA__gte=186).order_by('year', 'fTotal')

        stat_list = ['player', 'year']
        stat_list.extend(self.request.GET.getlist('include'))
        for stat in self.request.GET.getlist('include'):
            stat_list.append("f" + stat)
        stat_list.append("fTotal")

        if self.request.GET.get('year'):
            object_list = object_list.filter(year=self.request.GET.get('year'))

        if self.request.GET.get('min_pa'):
            object_list = object_list.filter(PA__gte=self.request.GET.get('min_pa'))

        context['field_names'] = HittingStatistics.objects.first().get_field_names()
        context['included_field_names'] = stat_list if self.request.GET.get('include') else HittingStatistics.objects.first().get_field_names()
        context['object_list'] = object_list.order_by('fTotal')
        context['year_list'] = HittingStatistics.objects.order_by().values_list('year', flat=True).distinct()
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('include'):
            stats_list = request.GET.getlist('include')
            for row in HittingStatistics.objects.all():
                total = 0
                for stat in stats_list:
                    total += getattr(row, "f" + stat)
                average = total/len(stats_list)
                row.fTotal = average
                row.save()
        return render(request, 'hitting_stats.html', context=self.get_context_data())


class PitchingStatsView(TemplateView):
    model = PitchingStatistics
    template_name = 'pitching_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = PitchingStatistics.objects.filter(IP__gte=10)

        stat_list = ['player', 'year']
        stat_list.extend(self.request.GET.getlist('include'))
        for stat in self.request.GET.getlist('include'):
            stat_list.append("f" + stat)
        stat_list.append("fTotal")

        if self.request.GET.get('year'):
            object_list = object_list.filter(year=self.request.GET.get('year'))

        if self.request.GET.get('min_ip'):
            object_list = object_list.filter(PA__gte=self.request.GET.get('min_ip'))

        context['field_names'] = PitchingStatistics.objects.first().get_field_names()
        context['included_field_names'] = stat_list if self.request.GET.get('include') else PitchingStatistics.objects.first().get_field_names()
        context['object_list'] = object_list
        context['year_list'] = PitchingStatistics.objects.order_by().values_list('year', flat=True).distinct()
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('include'):
            stat_list = request.GET.getlist('include')
            for row in PitchingStatistics.objects.all():
                total = 0
                for stat in stat_list:
                    total += getattr(row, "f" + stat)
                average = total/len(stat_list)
                row.fTotal = average
                row.save()
        return render(request, 'pitching_stats.html', context=self.get_context_data())
