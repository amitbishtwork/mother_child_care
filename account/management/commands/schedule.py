import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import datetime, timedelta
from account.models import VaccineStatus


class Command(BaseCommand):

	def handle(self, *args, **options):
		coming_vacinations = VaccineStatus.objects.filter(status='Pending',due_date__date=datetime.now())
		ivr_mapping = {"C":"1000083560","M":"1000083491"}
		contact_number = []
		for order in coming_vacinations:
			ivr_id = ivr_mapping["C"]
			start_time = str(datetime.now() + timedelta(minutes=5))
			end_time = str(datetime.now() + timedelta(minutes=25))
			contact_number.append(str(order.vaccine_for.contact)) 

		if contact_number:
			params= {
						"ivr_id": ivr_id,
						"timezone": "Asia/Kolkata",
						"priority": "1",
						"order_throttling": "10",
						"retry_duration": "15",
						"start_time": start_time[:16],
						"end_time": end_time[:16],
						"max_retry": "1",
						"call_scheduling": "[1, 1, 1, 1, 1, 1, 1]",
						"call_scheduling_start_time": "09:00",
						"call_scheduling_stop_time": "21:00",
						"k_number": "+919986734429",
						"additional_number":';'.join(contact_number),
						"is_transactional": "False"
					}
			headers = {"x-api-key":"OiYYz7MyCC1ZNqogqWHPj9kZQqBjuKJRaXpKnhMK",
						"Authorization":"6fffb5f6-d27d-4c1f-a04f-3112cb7f3f70"}

			url = 'https://kpi.knowlarity.com/Basic/v1/account/call/campaign'
			order = requests.post(url,json=params,headers=headers)
			print(order.text)

