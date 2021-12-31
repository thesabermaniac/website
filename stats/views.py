from django.shortcuts import render
from django.views.generic import *
from stats.models import HittingStatistics, Player, PitchingStatistics
from thesabermaniac.forms import TradeForm
from django.db.models import *
from django.conf import settings

from itertools import chain

class Home(TemplateView):
    template_name = 'home.html'


class BigBoardView(ListView):
    model = HittingStatistics
    template_name = 'stats_list.html'
    hitting_qs = HittingStatistics.objects.all()
    pitching_qs = PitchingStatistics.objects.all()

    def get_queryset(self):
        if self.request.GET.get('year'):
            self.hitting_qs = self.hitting_qs.filter(year=self.request.GET.get('year'))
            self.pitching_qs = self.pitching_qs.filter(year=self.request.GET.get('year'))
        if self.request.GET.get('proj'):
            self.hitting_qs = self.hitting_qs.filter(is_projection=self.request.GET.get('proj'), projection_system=self.request.GET.get('proj_sys'))
            self.pitching_qs = self.pitching_qs.filter(is_projection=self.request.GET.get('proj'), projection_system=self.request.GET.get('proj_sys'))
        if self.request.GET.get('min_pa'):
            self.hitting_qs = self.hitting_qs.filter(PA__gte=self.request.GET.get('min_pa'))
        if self.request.GET.get('min_ip'):
            self.pitching_qs = self.pitching_qs.filter(IP__gte=self.request.GET.get('min_ip'))
        return list(chain(self.hitting_qs, self.pitching_qs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context'] = context
        hitting_stats = []
        pitching_stats = []
        stat_list = ['player', 'year']
        for stat in self.request.GET.getlist('hitting'):
            hitting_stats.append("f" + stat)
        for stat in self.request.GET.getlist('pitching'):
            pitching_stats.append("f" + stat)
        stat_list.extend(hitting_stats)
        stat_list.extend(pitching_stats)
        stat_list.append('fTotal')
        for row in self.hitting_qs:
            total = 0
            for stat in hitting_stats:
                total += getattr(row, stat)
            average = total/len(hitting_stats) if len(hitting_stats) > 0 else 1
            context['fTotal_' + str(row)] = int(average)
        for row in self.pitching_qs:
            total = 0
            for stat in pitching_stats:
                total += getattr(row, stat)
            average = total/len(pitching_stats) if len(pitching_stats) > 0 else 1
            context['fTotal_' + str(row)] = int(average)
        context['hitting_fields'] = self.hitting_qs.first().get_field_names() if self.hitting_qs else ''
        context['pitching_fields'] = self.pitching_qs.first().get_field_names() if self.pitching_qs else ''
        context['year_list'] = list(set(HittingStatistics.objects.order_by().values_list('year', flat=True).distinct()) & set(PitchingStatistics.objects.order_by().values_list('year', flat=True).distinct()))
        context['included_field_names'] = stat_list
        context['hitting_stats'] = hitting_stats
        context['pitching_stats'] = pitching_stats
        context['bigboard'] = True
        return context


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
            self.model = self.model.filter(is_projection=self.request.GET.get('proj'), projection_system=self.request.GET.get('proj_sys'))

        if self.request.GET.get('year'):
            self.model = self.model.filter(year__in=self.request.GET.getlist('year'))

        if self.request.GET.get('min_pa'):
            self.model = self.model.filter(PA__gte=self.request.GET.get('min_pa'))

        if self.request.GET.get('min_ip'):
            self.model = self.model.filter(IP__gte=self.request.GET.get('min_ip'))

        context['field_names'] = self.model.first().get_field_names() if self.model else ''
        context['included_field_names'] = stat_list if self.request.GET.get('include') else self.model.first().get_field_names()
        context['object_list'] = self.model
        context['default_year'] = settings.DEFAULT_YEAR
        for row in self.model:
            total = 0
            for stat in self.request.GET.getlist('include'):
                total += getattr(row, "f" + stat)
            average = total/len(self.request.GET.getlist('include'))
            context['fTotal_' + str(row)] = int(average)
        context['context'] = context
        return context


class TradeAnalyzer(FormView):
    template_name = 'trade-analyzer.html'
    form_class = TradeForm
    success_url = '/trade-analyzer/'
    context = {}
    f_total = 0

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        name = form.data['name']
        id = form.data['fangraphs_id']
        player, created = Player.objects.get_or_create(fangraphs_id=id)
        try:
            hitting_stats, created = HittingStatistics.objects.get_or_create(player=player.fangraphs_id, year=2022)
            f_total = (hitting_stats.fOPS + hitting_stats.fAVG + hitting_stats.fHR + hitting_stats.fR + hitting_stats.fSB + hitting_stats.fRBI)/6
        except:
            try:
                pitching_stats, created = PitchingStatistics.objects.get_or_create(player=player.fangraphs_id, year=2022)
                f_total = (pitching_stats.fW + pitching_stats.fSO + pitching_stats.fSVH + pitching_stats.fERA + pitching_stats.fWHIP + pitching_stats.fK_BB)/6
            except Exception as e:
                print(e)
        context = self.get_context_data(**kwargs)
        context['fTotal'] = round(f_total)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(TradeAnalyzer, self).get_context_data(**kwargs)
        context['players'] = Player.objects.all()
        context['hitting_fScores'] = {hitter.player.fangraphs_id: round((hitter.fOPS + hitter.fAVG + hitter.fR + hitter.fRBI + hitter.fHR + hitter.fSB)/6) for hitter in HittingStatistics.objects.filter(year=2022)}
        context['pitching_fScores'] = {pitcher.player.fangraphs_id: round((pitcher.fERA + pitcher.fWHIP + pitcher.fW + pitcher.fSO + pitcher.fSVH + pitcher.fK_BB)/6) for pitcher in PitchingStatistics.objects.filter(year=2022)}
        return context

