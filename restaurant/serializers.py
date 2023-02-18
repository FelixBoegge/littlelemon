from django.contrib.auth.models import User
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from .models import Booking, Category, MenuItem, Cart, Order, OrderItem


class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        
        
class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    booking_time = serializers.SerializerMethodField(method_name='convert_booking_slot')
    class Meta:
        model = Booking
        fields = ['id', 'name', 'user', 'num_guests', 'booking_date', 'booking_time']
        extra_kwargs = {
            'booking_slot': {'min_value': 10, 'max_value': 22}
        }
        
    def convert_booking_slot(self, obj):
        if obj.booking_slot <= 12:
            ampm = ' AM'
            time = obj.booking_slot
        else:
            ampm = ' PM'
            time = obj.booking_slot - 12
        return str(time) + ampm
        

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
