from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Booking, Menu


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        

class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']