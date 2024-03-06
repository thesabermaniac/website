from django.core.management.base import BaseCommand
from stats.models import Player, HittingStatistics
from pybaseball import playerid_lookup
import pandas as pd


class Command(BaseCommand):
    help = "Moves player stats from csv file to the database"

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('year', type=int)
        parser.add_argument('--is_proj', action='store_true')
        parser.add_argument('-proj_sys', type=str, default=None)

    def handle(self, *args, **options):
        stats_df = pd.read_csv(options['file_name']).dropna(axis=1, how='all')
        if 'PlayerId' in stats_df.columns:
            stats_df.rename(columns={'PlayerId': 'playerid'}, inplace=True)
        proj = options['proj_sys'] if 'proj' in options else ''

        if 'PA' not in stats_df.columns and 'AB' in stats_df.columns and 'BB' in stats_df.columns:
            stats_df['PA'] = stats_df['AB'] + stats_df['BB']

        if 'playerid' not in stats_df.columns:
            stats_df['playerid'] = stats_df['Name'].apply(self.get_playerid, args=(options['year'], proj))

        for index, row in stats_df.iterrows():
            player = self.get_player_by_playerid(row['playerid'], row['Name'])
            if player:
                hitting_stats, created = HittingStatistics.objects.get_or_create(player=player, year=options['year'],
                                                                                 is_projection=options['is_proj'],
                                                                                 projection_system=options['proj_sys'])
                for col, value in row.items():
                    if col in hitting_stats.get_field_names():
                        setattr(hitting_stats, col, value)
                hitting_stats.save()

    def get_playerid(self, name, year, proj):
        name_parts = name.split(' ')
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])
        player_df = playerid_lookup(last=last_name, first=first_name, ignore_accents=True)
        if player_df.empty and len(name_parts) > 2:
            player_df = playerid_lookup(last=name_parts[1:][0], first=first_name, ignore_accents=True)
        elif player_df.empty and '.' in (first_name or '.' in last_name):
            first_name = ' '.join(first_name.split('.'))
            last_name = ' '.join(last_name.split('.'))
            player_df = playerid_lookup(last=last_name, first=first_name, ignore_accents=True)

        try:
            return player_df.loc[0]['key_fangraphs']
        except KeyError:
            error_key = f'{name},{year},{proj}' if proj else f'{name},{year}'
            with open('failed_names.txt', 'r') as error_log:
                errors = set(error_log.read().splitlines())
                errors.add(error_key)
            with open('failed_names.txt', 'w') as error_log:
                error_log.write('\n'.join(e for e in errors if e) + '\n')
            return None

    def get_player_by_playerid(self, playerid, name):
        if playerid:
            player, created = Player.objects.get_or_create(fangraphs_id=playerid)
            if created:
                player.name = name
        else:
            player, created = Player.objects.get_or_create(name=name)
        player.save()
        return player
