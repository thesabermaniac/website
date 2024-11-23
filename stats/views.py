from django.views.generic import *
from stats.models import HittingStatistics, Player, PitchingStatistics
from django.conf import settings
from django.db.models import Q
from collections import defaultdict

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
        objects = context['object_list']
        players = {o.player for o in objects}
        final_stats = []

        player_statistics = defaultdict(list)
        for obj in objects:
            player_statistics[obj.player].append(obj)

        for p in players:
            stats = player_statistics[p]
            player_stats = {'player': str(p)}
            hitting_total = 0
            pitching_total = 0
            for stat in stats:
                if type(stat) == HittingStatistics:
                    hitting_statistics = {s: getattr(stat, s) for s in hitting_stats}
                    player_stats.update(hitting_statistics)
                    hitting_total = sum(hitting_statistics.values())/len(hitting_statistics.values())
                elif type(stat) == PitchingStatistics:
                    pitching_statistics = {s: getattr(stat, s) for s in pitching_stats}
                    player_stats.update(pitching_statistics)
                    pitching_total = sum(pitching_statistics.values())/len(pitching_statistics.values())
                player_stats['year'] = stat.year
            player_stats['fTotal'] = round(hitting_total + pitching_total)
            final_stats.append(player_stats)
        context['object_list'] = final_stats
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
        # stat_list.append("fTotal")

        if self.request.GET.get('proj'):
            self.model = self.model.filter(is_projection=self.request.GET.get('proj'), projection_system=self.request.GET.get('proj_sys'))

        if self.request.GET.get('year'):
            self.model = self.model.filter(year__in=self.request.GET.getlist('year'))

        if self.request.GET.get('min_pa'):
            self.model = self.model.filter(PA__gte=self.request.GET.get('min_pa'))

        if self.request.GET.get('min_ip'):
            self.model = self.model.filter(IP__gte=self.request.GET.get('min_ip'))

        context['field_names'] = self.model.first().get_field_names() if self.model else ''
        included_fields = stat_list if self.request.GET.get('include') else self.model.first().get_field_names()
        context['included_field_names'] = included_fields + ['fTotal']
        context['object_list'] = self.model
        context['default_year'] = settings.DEFAULT_YEAR
        final_stats = []
        for row in self.model:
            player_stats = {}
            for stat in included_fields:
                player_stats[stat] = getattr(row, stat)
            fstats = [v for k, v in player_stats.items() if k.startswith('f')]
            average = sum(fstats)/len(fstats)
            player_stats['fTotal'] = int(average)
            final_stats.append(player_stats)
        context['object_list'] = final_stats
        context['context'] = context
        return context


class TradeAnalyzer(TemplateView):
    template_name = 'trade-analyzer.html'

    def get_context_data(self, **kwargs):
        context = super(TradeAnalyzer, self).get_context_data(**kwargs)
        query = Q(year=2024, projection_system='steamer') | Q(year=2025, projection_system='zips') | Q(year=2026, projection_system='zips')
        hitters = HittingStatistics.objects.filter(query)
        pitchers = PitchingStatistics.objects.filter(query)

        all_players = set([player_object.player for player_object in pitchers] + [player_object.player for player_object in hitters])
        print(f'players view: {len(all_players)}')
        context['players'] = all_players

        hitting_fScores = {}
        for hitter in hitters:
            player_id = hitter.player.fangraphs_id
            if player_id not in hitting_fScores:
                hitting_fScores[player_id] = {}
            hitting_fScores[player_id][hitter.year] = round((hitter.fOPS + hitter.fAVG + hitter.fR + hitter.fRBI + hitter.fHR + hitter.fSB)/6)

        pitching_fScores = {}
        for pitcher in pitchers:
            player_id = pitcher.player.fangraphs_id
            if player_id not in pitching_fScores:
                pitching_fScores[player_id] = {}
            pitching_fScores[player_id][pitcher.year] = round((pitcher.fERA + pitcher.fWHIP + pitcher.fW + pitcher.fSO + pitcher.fSVH + pitcher.fK_BB)/6)

        context['hitting_fScores'] = hitting_fScores
        context['pitching_fScores'] = pitching_fScores
        # context['hitting_fScores'] = {hitter.player.fangraphs_id: round((hitter.fOPS + hitter.fAVG + hitter.fR + hitter.fRBI + hitter.fHR + hitter.fSB)/6) for hitter in HittingStatistics.objects.filter(year=2024, projection_system='steamer')}
        # context['pitching_fScores'] = {pitcher.player.fangraphs_id: round((pitcher.fERA + pitcher.fWHIP + pitcher.fW + pitcher.fSO + pitcher.fSVH + pitcher.fK_BB)/6) for pitcher in PitchingStatistics.objects.filter(year=2024, projection_system='steamer')}
        return context

