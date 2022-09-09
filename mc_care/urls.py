
import imp
from django.contrib import admin
from django.urls import path
from .views import create_appointment
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from account.views import TestView, UserAPIView,LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserAPIView.as_view(), name='user'),
    path('api/test/', TestView.as_view(), name='user'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('create_appointment/', create_appointment, name='create_appointment')
]
