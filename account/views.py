from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import jwt
from rest_framework.generics import  RetrieveAPIView
from django.db.models import Q
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import serializers
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Appointment, VaccineStatus


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('id', 'email')


# views ===================================================
class VaccineStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *a, **kw):
        myuser = self.request.user
        User = get_user_model()

        vaccine_status = VaccineStatus.objects.select_related('vaccine_for', 'vaccine_name').filter(
            Q(vaccine_for=myuser) | Q(vaccine_for__parent=myuser),
            vaccine_for__user_type='C'
        ).values('id', 'vaccine_for__first_name', 'vaccine_for__last_name',
                 'vaccine_for__birth_day',
                 'vaccine_for__parent__first_name',
                 'vaccine_name__vaccine_name', 'vaccine_name__total_doses',
                 'vaccine_name__age_given',
                 'dosage_count', 'status', 'due_date', 'applied_on')

        print(vaccine_status)
        return Response(vaccine_status, content_type='application/json')


class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *a, **kw):
        ap_type = self.request.GET.get('type', 'patient')
        myuser = self.request.user
        ap_type = myuser.user_type
        print(myuser)
        values_list = ('appointment_date', 'appointment_of__email', 'appointment_of__first_name',
                    'appointment_of__last_name', 'appointment_of__contact', 'doctor_name__email', 'doctor_name__first_name',
                    'doctor_name__last_name')

        if myuser.is_staff:
            print('get starff full')
            appointment = Appointment.objects.select_related('appointment_of', 'doctor_name').all().values(
                *values_list).all()
        else:
            print(ap_type)
            if ap_type == 'D':
                appointment = Appointment.objects.select_related('appointment_of', 'doctor_name'
                                                                 ).filter(doctor_name=myuser).values(*values_list)
            elif ap_type in ('M', 'C'):
                appointment = Appointment.objects.select_related('appointment_of', 'doctor_name').filter(
                    appointment_of=myuser
                ).values(*values_list)

        return Response(appointment, content_type='application/json')


class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kw):
        return Response("hw")




class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request, *args, **kw):

        params = request.data

        email = params.get('email')
        password = params.get('password')

        user = authenticate(username=email, password=password)
        if user:
            payload = RefreshToken.for_user(user)
            auth_token = str(payload.access_token)
            print(auth_token)
            return Response({"email":user.email,"user_type":user.user_type,"id":user.id,"name":user.first_name,"email":user.email,"contact":user.contact,"token":auth_token})
        return Response({"error":"Invalid username/password"},status=400)