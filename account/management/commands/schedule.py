import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import datetime, timedelta
from account.models import VaccineStatus


class Command(BaseCommand):

	def handle(self, *args, **options):
		 coming_vacinations = VaccineStatus.objects.filter(status='Pending',due_date__date=datetime.now()+timedelta(days=2))
		 


