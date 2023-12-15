from django.core.management.base import BaseCommand, CommandError
from stats.models import PitchingStatistics
from django.db.models import *


class Command(BaseCommand):
    help = 'Generate fStats for pitching stats'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('-proj_sys', type=str, default=None)

    def handle(self, *args, **options):
        stat_list = ['W', 'L', 'ERA', 'WHIP', 'G', 'GS', 'CG', 'ShO', 'SV', 'HLD', 'BS',
                     'IP', 'TBF', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'HBP', 'WP', 'SO', 'SVH', 'K_BB']
        reverse_list = ['L', 'ERA', 'WHIP', 'BS', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'HBP', 'WP']
        rate_stats = ['ERA', 'WHIP', 'K_BB']
        qs = PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys'], IP__gte=10).annotate(
            weighted_ERA=F('ERA') * F('IP'),
            weighted_WHIP=F('WHIP') * F('IP'),
            weighted_K_BB=F('K_BB') * F('IP')
        )
        aggregated_stats = qs.aggregate(
            Max('W'),
            Max('L'),
            Max('G'),
            Max('GS'),
            Max('CG'),
            Max('ShO'),
            Max('SV'),
            Max('HLD'),
            Max('BS'),
            Max('IP'),
            Max('TBF'),
            Max('H'),
            Max('R'),
            Max('ER'),
            Max('HR'),
            Max('BB'),
            Max('IBB'),
            Max('HBP'),
            Max('WP'),
            Max('SO'),
            Max('SVH'),
            Max('ERA'),
            Max('WHIP'),
            Max('K_BB'),
            Max('weighted_ERA'),
            Max('weighted_WHIP'),
            Max('weighted_K_BB'),
            Min('W'),
            Min('L'),
            Min('G'),
            Min('GS'),
            Min('CG'),
            Min('ShO'),
            Min('SV'),
            Min('HLD'),
            Min('BS'),
            Min('IP'),
            Min('TBF'),
            Min('H'),
            Min('R'),
            Min('ER'),
            Min('HR'),
            Min('BB'),
            Min('IBB'),
            Min('HBP'),
            Min('WP'),
            Min('SO'),
            Min('SVH'),
            Min('ERA'),
            Min('WHIP'),
            Min('K_BB'),
            Min('weighted_ERA'),
            Min('weighted_WHIP'),
            Min('weighted_K_BB')
        )
        qs = qs.annotate(
            weighted_scaled_ERA=((aggregated_stats['ERA__max'] - F('ERA'))/(aggregated_stats['ERA__max']-aggregated_stats['ERA__min'])*100) * F('IP'),
            weighted_scaled_WHIP=((aggregated_stats['WHIP__max'] - F('WHIP'))/(aggregated_stats['WHIP__max']-aggregated_stats['WHIP__min'])*100) * F('IP'),
            weighted_scaled_K_BB=((F('K_BB') - aggregated_stats['K_BB__min'])/(aggregated_stats['ERA__max']-aggregated_stats['ERA__min'])*100) * F('IP'),
        )
        scaled_aggregates = qs.aggregate(
            Max('weighted_scaled_ERA'),
            Max('weighted_scaled_WHIP'),
            Max('weighted_scaled_K_BB'),
            Min('weighted_scaled_ERA'),
            Min('weighted_scaled_WHIP'),
            Min('weighted_scaled_K_BB'),
        )
        for row in qs:
            for stat in stat_list:
                f_stat = 'f' + stat
                stat_val = getattr(row, stat)
                max_stat = aggregated_stats[f'{stat}__max']
                min_stat = aggregated_stats[f'{stat}__min']
                if max_stat == 0:
                    continue
                if stat in reverse_list:
                    result = (max_stat - stat_val)/(max_stat - min_stat)*100
                else:
                    result = (stat_val - min_stat)/(max_stat - min_stat)*100
                if stat in rate_stats:
                    weighted_stat = result * getattr(row, 'IP')
                    result = (weighted_stat - scaled_aggregates[f'weighted_scaled_{stat}__min'])/(scaled_aggregates[f'weighted_scaled_{stat}__max'] - scaled_aggregates[f'weighted_scaled_{stat}__min']) * 100
                setattr(row, f_stat, int(result))
            row.save()
