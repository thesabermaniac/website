from django.core.management.base import BaseCommand, CommandError
from stats.models import HittingStatistics
from django.db.models import *


class Command(BaseCommand):
    help = 'Generate fStats for hitting stats'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('proj_sys', type=str, default=None)

    def handle(self, *args, **options):
        stat_list = ['G', 'PA', 'HR', 'R', 'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS', 'AVG', 'OBP', 'SLG', 'OPS']
        reverse_list = ['SO', 'CS']
        rate_stats = ['AVG', 'OBP', 'SLG', 'OPS']
        qs = HittingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys'])
        for stat in stat_list:
            fStat = "f" + stat
            max = qs.aggregate(Max(stat))[stat + "__max"]
            min_stat = qs.aggregate(Min(stat))[stat + "__min"]
            control = 100/max if max else 0
            if stat in reverse_list:
                control = 100/(min_stat - max) if (max and min_stat) else 0
            for row in qs:
                result = (((getattr(row, stat) or 0) * control) + 100) if stat in reverse_list else (getattr(row, stat) or 0) * control
                setattr(row, fStat, int(result))
                row.save()
                if stat == stat_list[-1]:
                    for statistic in rate_stats:
                        frate = getattr(row, 'f' + statistic) or 0
                        setattr(row, 'f' + statistic, (frate + row.fPA)/2)
                        row.save()
        for statistic in rate_stats:
            max = qs.aggregate(Max('f' + statistic))['f' + statistic + '__max']
            control = 100/max if max else 0
            for row in qs:
                result = getattr(row, 'f' + statistic) or 0 * control
                setattr(row, 'f' + statistic, int(result))
                row.save()
