from django.core.management.base import BaseCommand
from stats.models import Player


class Command(BaseCommand):
    help = "Remove all records from db"

    def handle(self, *args, **options):
        players = Player.objects.all()
        players.delete()
        print(players)
