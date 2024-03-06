from django.core.management.base import BaseCommand
from stats.models import PitchingStatistics, HittingStatistics


class Command(BaseCommand):
    help = "Drop a year of stats from the database"

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('-proj_sys', type=str, default=None)

    def handle(self, *args, **options):
        HittingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys']).delete()
        PitchingStatistics.objects.filter(year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys']).delete()
