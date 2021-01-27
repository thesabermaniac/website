from django.core.management.base import BaseCommand
from stats.models import PitchingStatistics, HittingStatistics
from itertools import chain


class Command(BaseCommand):
    help = "Set projection system of stats"

    def add_arguments(self, parser):
        parser.add_argument('system', type=str)

    def handle(self, *args, **options):
        hitting_qs = HittingStatistics.objects.filter(is_projection=True)
        pitching_qs = PitchingStatistics.objects.filter(is_projection=True)
        for stat in list(chain(hitting_qs, pitching_qs)):
            stat.projection_system = options['system']
            stat.save()
