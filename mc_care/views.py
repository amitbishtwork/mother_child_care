from django import views
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from account.models import Appointment
from django.conf import settings
from datetime import datetime
import datetime as dt
import traceback


def create_appointment(request):
    try:
        patient_number = request.GET.get('a')
        patient_number = "+{}".format(patient_number)
        print(patient_number)
        auth_user = get_user_model()
        print(auth_user)
        patient = auth_user.objects.filter(contact=patient_number).first()
        if not patient:
            return HttpResponse('not crated')
        doctor = auth_user.objects.get(email='doctor@doctor.com')
        schedule_date = datetime.now() + dt.timedelta(days=2)
        aa = Appointment.objects.filter(appointment_of=patient, appointment_date__date=schedule_date.date())
        if aa:
            return HttpResponse('appointment already created')
        ap = Appointment(appointment_of=patient, appointment_date=schedule_date, doctor_name=doctor)
        ap.save()
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        return HttpResponse('somethig went wrong')
    else:
        return HttpResponse('done')