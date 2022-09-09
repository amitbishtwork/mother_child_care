from django.shortcuts import render
from django.conf import settings
import jwt
from rest_framework.generics import  RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import serializers
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('id', 'email')
        

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