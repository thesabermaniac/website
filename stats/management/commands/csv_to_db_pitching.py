import csv

from django.core.management.base import BaseCommand
from stats.models import Player, PitchingStatistics
from pybaseball import playerid_lookup


class Command(BaseCommand):
    help = "Move pitching stats from csv file to the database"

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('-proj_sys', type=str, default=None, )

    def handle(self, *args, **options):
        with open(options['file_name'], 'r', encoding='utf8') as file:
            csv_reader = csv.DictReader(file)
            csv_reader.fieldnames[0] = 'Name'
            for row in csv_reader:
                name = row.get('Name')
                if 'playerid' in row:
                    player, player_created = Player.objects.get_or_create(fangraphs_id=row.get('playerid'))
                else:
                    name_parts = name.split(' ')
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:])
                    player_id = playerid_lookup(last=last_name, first=first_name, fuzzy=True)
                    player, player_created = Player.objects.get_or_create(fangraphs_id=player_id.loc[0]['key_fangraphs'])
                    if player.position != 'P' and player_id.shape[0] > 1:
                        player, player_created = Player.objects.get_or_create(fangraphs_id=player_id.loc[1]['key_fangraphs'])
                if player_created:
                    player.name = row.get('Name')
                player.save()
                statistic, stat_created = PitchingStatistics.objects.get_or_create(player=player, year=options['year'], is_projection=options['is_proj'], projection_system=options['proj_sys'])
                statistic.HLD = 0
                statistic.SV = 0
                for item in row.items():
                    if item[0] in statistic.get_field_names():
                        setattr(statistic, item[0], item[1])
                statistic.save()
