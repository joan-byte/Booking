# reservas/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default groups for socios'

    def handle(self, *args, **kwargs):
        groups = ['Socios Deportivos', 'Socios Paseantes']
        for group in groups:
            Group.objects.get_or_create(name=group)
        self.stdout.write(self.style.SUCCESS('Successfully created default groups'))