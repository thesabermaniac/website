from pybaseball import batting_stats
from django.core.management.base import BaseCommand
from stats.models import Player, HittingStatistics


class Command(BaseCommand):
    help = 'Import Batting stats from a given year'

    def add_arguments(self, parser):
        parser.add_argument('-y', '--year', type=int, default=None)

    def handle(self, *args, **options):
        year = options['year']
        data = batting_stats(year, qual=1)
        data_dict = data.to_dict('list')
        players = []
        for i, player in enumerate(data_dict['IDfg']):
            player, created = Player.objects.get_or_create(fangraphs_id=player)
            if created:
                player.name = data_dict['Name'][i]
                player.save()
            players.append(player)
        fields = HittingStatistics().get_field_names()
        for i, p in enumerate(players):
            statistics, created = HittingStatistics.objects.get_or_create(player=p, year=year, is_projection=False)
            for field in fields:
                if field in data_dict.keys():
                    setattr(statistics, field, data_dict[field][i])
            statistics.save()
