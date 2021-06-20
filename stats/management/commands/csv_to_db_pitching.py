import csv

from django.core.management.base import BaseCommand, CommandError
from stats.models import Player, PitchingStatistics
from fractions import Fraction as frac


class Command(BaseCommand):
    help = "Move pitching stats from csv file to the database"

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('-proj_sys', type=str, default=None, )

    def handle(self, *args, **options):
        with open(options['file_name'], 'r') as file:
            csv_reader = csv.DictReader(file)
            csv_reader.fieldnames[0] = 'Name'
            for row in csv_reader:
                name_list = row.get('Name').split()
                fName = name_list[0]
                lName = name_list[1]
                player, player_created = Player.objects.get_or_create(fName=fName,
                                                                      lName=lName)
                player.save()
                statistic, stat_created = PitchingStatistics.objects.get_or_create(player=player, year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys'])
                statistic.HLD = 0
                statistic.SV = 0
                for item in row.items():
                    if item[0] in statistic.get_field_names():
                        setattr(statistic, item[0], item[1])
                statistic.save()
