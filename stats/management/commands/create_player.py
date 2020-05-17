from django.core.management.base import BaseCommand, CommandError
from stats.models import Player


class Command(BaseCommand):
    help = 'Creates new player'

    def handle(self, *args, **options):
        Player.objects.create(fName='Mike', lName='Trout', position='CF')
