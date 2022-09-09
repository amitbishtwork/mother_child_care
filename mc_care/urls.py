
import imp
from django.contrib import admin
from django.urls import path
from .views import create_appointment
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from account.views import TestView, UserAPIView, AppointmentView, VaccineStatusView, AppointmentView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserAPIView.as_view(), name='user'),
    path('api/test/', TestView.as_view(), name='user'),
    path('create_appointment/', create_appointment, name='create_appointment'),
    path('api/v1/appointment/', AppointmentView.as_view(), name='appointment'),
    path('api/v1/vaccine_status/', VaccineStatusView.as_view(), name='vaccine-status'),
]
