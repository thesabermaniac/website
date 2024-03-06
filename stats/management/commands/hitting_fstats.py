from django.core.management.base import BaseCommand, CommandError
from stats.models import HittingStatistics
from django.db.models import *


class Command(BaseCommand):
    help = 'Generate fStats for hitting stats'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('-proj_sys', type=str, default=None)

    def handle(self, *args, **options):
        stat_list = ['G', 'PA', 'HR', 'R', 'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS']
        reverse_list = ['SO', 'CS']
        rate_stats = ['AVG', 'OBP', 'SLG', 'OPS']
        qs = HittingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys'])
        aggregated_stats = qs.annotate(
            weighted_AVG=F('AVG') * F('PA'),
            weighted_OBP=F('OBP') * F('PA'),
            weighted_SLG=F('SLG') * F('PA'),
            weighted_OPS=F('OPS') * F('PA'),
        ).aggregate(
            Max('G'),
            Max('PA'),
            Max('HR'),
            Max('R'),
            Max('RBI'),
            Max('BB'),
            Max('IBB'),
            Max('SO'),
            Max('HBP'),
            Max('SF'),
            Max('SH'),
            Max('GDP'),
            Max('SB'),
            Max('CS'),
            Max('weighted_AVG'),
            Max('weighted_OBP'),
            Max('weighted_SLG'),
            Max('weighted_OPS'),
            Min('G'),
            Min('PA'),
            Min('HR'),
            Min('R'),
            Min('RBI'),
            Min('BB'),
            Min('IBB'),
            Min('SO'),
            Min('HBP'),
            Min('SF'),
            Min('SH'),
            Min('GDP'),
            Min('SB'),
            Min('CS'),
            Min('weighted_AVG'),
            Min('weighted_OBP'),
            Min('weighted_SLG'),
            Min('weighted_OPS')
        )
        for row in qs:
            for stat in stat_list:
                f_stat = "f" + stat
                stat_val = getattr(row, stat) * getattr(row, 'PA') if stat in rate_stats else getattr(row, stat)
                max_stat = aggregated_stats[f'weighted_{stat}__max'] if stat in rate_stats else aggregated_stats[f'{stat}__max']
                min_stat = aggregated_stats[f'weighted_{stat}__min'] if stat in rate_stats else aggregated_stats[f'{stat}__min']
                if min_stat - max_stat == 0:
                    continue
                if stat in reverse_list:
                    result = (max_stat - stat_val)/(max_stat - min_stat)*100
                else:
                    result = (stat_val - min_stat)/(max_stat - min_stat)*100
                setattr(row, f_stat, int(result))
            row.save()
