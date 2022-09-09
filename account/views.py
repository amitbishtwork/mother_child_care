from django.shortcuts import render
from django.conf import settings

from rest_framework.generics import  RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


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