from django import views
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from account.models import Appointment
from django.conf import settings
from datetime import datetime
import datetime as dt
import traceback


def create_appointment(request):
    try:
        patient_type = request.GET.get('type')

        patient_number = request.GET.get('phone_number')
        patient_number = "+{}".format(patient_number.strip())
        print(patient_number)
        auth_user = get_user_model()
        patient = auth_user.objects.filter(contact=patient_number, user_type=patient_type).first()
        print(patient)
        if not patient:
            return JsonResponse({'message': 'not created'}, status=400)
        doctor = auth_user.objects.get(email='doctor@doctor.com')
        schedule_date = datetime.now()
        aa = Appointment.objects.select_related('appointment_of').filter(appointment_of=patient, 
                                                                         appointment_date__date=schedule_date.date()
                                                                         )
        if aa:
            return JsonResponse({"message": 'appointment already registerred'})

        ap = Appointment(appointment_of=patient, appointment_date=schedule_date, doctor_name=doctor)
        ap.save()
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        return JsonResponse({'message': 'something wrong'}, status=400)
    else:
        return JsonResponse({'messgage': 'success'})