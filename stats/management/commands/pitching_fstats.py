from django.core.management.base import BaseCommand, CommandError
from stats.models import PitchingStatistics
from django.db.models import *


class Command(BaseCommand):
    help = 'Generate fStats for pitching stats'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')

    def handle(self, *args, **options):
        stat_list = ['W', 'L', 'ERA', 'WHIP', 'G', 'GS', 'CG', 'ShO', 'SV', 'HLD', 'BS',
                     'IP', 'TBF', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'HBP', 'WP', 'SO']
        reverse_list = ['L', 'ERA', 'WHIP', 'BS', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'HBP', 'WP']
        rate_stats = ['ERA', 'WHIP']
        for stat in stat_list:
            fStat = "f" + stat
            max = PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj']).aggregate(Max(stat))[stat + "__max"] or 0
            min_stat = PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj']).aggregate(Min(stat))[stat + "__min"] or 0
            control = 100/max if max != 0 else 0
            if stat in reverse_list:
                control = 100/(min_stat - max) if max != 0 and min_stat != 0 else 0
            for row in PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj']):
                if getattr(row, stat):
                    result = (getattr(row, stat) * control) + 100 if stat in reverse_list else getattr(row, stat) * control
                else:
                    result = 0
                setattr(row, fStat, int(result))
                row.save()
                if stat == stat_list[-1]:
                    for statistic in rate_stats:
                        frate = getattr(row, "f" + statistic)
                        setattr(row, "f" + statistic, (frate + row.fIP)/2)
                        fTotal = 0
                        for score in stat_list:
                            fTotal += getattr(row, "f" + score)
                        row.fTotal = int(fTotal)/len(stat_list)
                        row.save()
        for statistic in rate_stats:
            max = PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj']).aggregate(Max("f" + statistic))['f' + statistic + '__max'] or 0
            control = 100/max if max !=0 else 0
            for row in PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj']):
                result = getattr(row, 'f' + statistic) * control
                setattr(row, 'f' + statistic, int(result))
                row.save()
