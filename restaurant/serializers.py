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
    class Meta:
        model = Booking
        fields = ['id', 'name', 'user', 'num_guests', 'booking_date', 'booking_slot']
        extra_kwargs = {
            'booking_slot': {'min_value': 10, 'max_value': 22}
        }       
   
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'category', 'price', 'inventory', 'featured']
        

class MenuItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.CharField(source='menuitem.title', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class CartCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = '__all__'
        

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.CharField(source='menuitem.title', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']
        

class OrderItemCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    delivery_crew = serializers.CharField(source='delivery_crew.username', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items','total', 'delivery_crew', 'status', 'date']
        
        
class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'