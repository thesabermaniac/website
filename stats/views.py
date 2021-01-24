from django.shortcuts import render
from django.views.generic import *
from stats.models import HittingStatistics, Player, PitchingStatistics
from django.db.models import *
from django.conf import settings


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


class StatsListView(ListView):
    model = None
    template_name = 'stats_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.model = self.model.objects.all()
        context['year_list'] = self.model.order_by().values_list('year', flat=True).distinct()

        stat_list = ['player', 'year']
        stat_list.extend(self.request.GET.getlist('include'))
        for stat in self.request.GET.getlist('include'):
            stat_list.append("f" + stat)
        stat_list.append("fTotal")

        if self.request.GET.get('proj'):
            self.model = self.model.filter(is_projection=self.request.GET.get('proj'))

        if self.request.GET.get('year'):
            self.model = self.model.filter(year__in=self.request.GET.getlist('year'))

        if self.request.GET.get('min_pa'):
            self.model = self.model.filter(PA__gte=self.request.GET.get('min_pa'))

        if self.request.GET.get('min_ip'):
            self.model = self.model.filter(IP__gte=self.request.GET.get('min_ip'))

        context['field_names'] = self.model.first().get_field_names() if self.model else ''
        context['included_field_names'] = stat_list if self.request.GET.get('include') else self.model.first().get_field_names()
        context['object_list'] = self.model.order_by('fTotal')
        context['default_year'] = settings.DEFAULT_YEAR
        for row in self.model:
            total = 0
            for stat in self.request.GET.getlist('include'):
                total += getattr(row, "f" + stat)
            average = total/len(self.request.GET.getlist('include'))
            context['fTotal_' + str(row)] = int(average)
        context['context'] = context
        return context
