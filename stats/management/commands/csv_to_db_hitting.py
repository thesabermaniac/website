import csv

from django.core.management.base import BaseCommand, CommandError
from stats.models import Player, HittingStatistics


class Command(BaseCommand):
    help = "Moves player stats from csv file to the database"

    def handle(self, *args, **options):
        with open('hitting_proj_2020.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            csv_reader.fieldnames[0] = 'Name'
            for row in csv_reader:
                # print(row)
                name_list = row.get('Name').split()
                fName = name_list[0]
                lName = name_list[1]
                player, player_created = Player.objects.get_or_create(fName=fName,
                                                                      lName=lName)
                player.save()
                statistic, stat_created = HittingStatistics.objects.get_or_create(player=player, year=2020, is_projection=True)
                for item in row.items():
                    if item[0] in statistic.get_field_names():
                        setattr(statistic, item[0], item[1])
                statistic.save()

