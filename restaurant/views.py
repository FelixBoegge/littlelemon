from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.views.generic.edit import FormView

from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from djoser.utils import login_user, logout_user
from djoser.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .models import Booking, Category, MenuItem, Cart, Order 
from .serializers import (UserSerializer, BookingSerializer, CategorySerializer,
                          MenuItemSerializer, MenuItemCreateSerializer,
                          CartSerializer, CartCreateSerializer,
                          OrderItemCreateSerialzer,
                          OrderSerializer, OrderCreateSerializer)
from .forms import BookingForm, SignupForm, LoginForm

from datetime import datetime
import json, requests

User = get_user_model()

class HomeView(APIView):

    def get(self, request):
        return render(request, 'index.html')

class AboutView(APIView):
    def get(self, request):
        return render(request, 'about.html')

class MenuView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('loginform')
        else:
            #print('##############', 'YES')
            categories = Category.objects.all()
            context = {'menu': categories}
            token = Token.objects.get(user=request.user.id).key
            context['Authorization'] = 'Token ' + token
            #print('##############', token)
            return render(request, 'menu.html', context) 

class CategoryView(APIView):
    def get(self, request, category):
        items = MenuItem.objects.all()
        if category:
            items = items.filter(category__slug=category)
        category_name = Category.objects.get(slug=category).title
        context = {'menuitems': items,
                   'category': category_name}
        return render(request, 'category.html', context)

class SingleMenuItemView(APIView):
    def get(self, request, pk):
        if pk: 
            menuitem = MenuItem.objects.get(pk=pk) 
        else: 
            menuitem = "" 
        return render(request, 'menuitem.html', {"menuitem": menuitem}) 

class BookView(APIView):
    form = BookingForm()
    
    def get(self, request):
        return render(request, 'book.html')
    
    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
        context = {'form':form}
        return render(request, 'book.html', context)

class BookingsView(APIView):
    @csrf_exempt
    def post(self, request):
        data = json.load(request)
        exist = Booking.objects.filter(booking_date=data['booking_date']).filter(
            booking_slot=data['booking_slot']).exists()
        if exist==False:
            booking = Booking(
                name=data['name'],
                user = 'felix',
                num_guests=data['num_guests'],
                booking_date=data['booking_date'],
                booking_slot=data['booking_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    def get(self, request):
        date = request.GET.get('date',datetime.today().date())
        bookings = Booking.objects.all().filter(booking_date=date)
        serialized_bookings = serializers.serialize('json', bookings)
        return HttpResponse(serialized_bookings, content_type='application/json')

class ReservationsView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.GET.get('date',datetime.today().date())
        bookings = Booking.objects.all()
        return render(request, 'bookings.html', {'bookings': bookings})

class SignupFormView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    #success_url = '/user-created/'
    def form_valid(self, form):
        return super().form_valid(form)
    
class UserCreateSuccessView(APIView):
    def get(self, request):
        success_messege = "<html><body><h1>Successfully created new User!</h1></body></html>"
        return HttpResponse(success_messege)

class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    def form_valid(self, form):
        return super().form_valid(form)

class UserCreateView(UserViewSet):
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            context = {'data': self.retrieve(request, *args, **kwargs)}
            return render(request, 'profile.html', context)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

class LoginView(TokenCreateView):
    def _action(self, serializer):
        token = login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return redirect('home')
    
class LogoutView(TokenDestroyView):
    def post(self, request):
        logout_user(request)
        return redirect('home')

class UsersView(APIView):
    @csrf_exempt
    def post(self, request):
        new_user_data = json.load(request)
        exist = User.objects.filter(username=new_user_data['username']).exists()
        if exist==False:
            new_user = User(
                username = new_user_data['username'],
                first_name = new_user_data['first_name'],
                last_name = new_user_data['last_name'],
                email = new_user_data['email'],
                password = new_user_data['password'],
            )
            #serializer = UserCreateSerializer(data=new_user)
            #if serializer.is_valid():
            new_user.save()
            return Response({'status': 'succesfully registered'}, status.HTTP_201_CREATED)
        else:
            return HttpResponse("{'error':1}", content_type='application/json')


class CartView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        carts = Cart.objects.filter(user=user_id)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @csrf_exempt
    def post(self, request):
        print('###########', 'here')
        data = json.load(request)
        user_id = Token.objects.get(key=request.auth.key).user_id
        menuitem_id = MenuItem.objects.get(id=data['menuitem']).pk
        quantity = request.data['num_items']
        unit_price = MenuItem.objects.get(pk=menuitem_id).price
        price = quantity * unit_price
        cart_item = Cart(
            user = user_id,
            menuitem =  menuitem_id,
            quantity = quantity,
            unit_price = unit_price,
            price = price
        )
        cart_item.save()
        return redirect('home')
        
        #serializer = CartCreateSerializer(data=cart_item)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response({'status': 'successfully added cartitem',
        #                     'data': serializer.data}, status.HTTP_201_CREATED)
        #return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        carts = Cart.objects.filter(user=user_id)
        num_carts = len(carts)
        if num_carts == 0:
            return Response({'status': 'no cartitems in cart'}, status.HTTP_200_OK)
        carts.delete()
        return Response({'status': f'successfully deleted {num_carts} cartitems from cart'}, status.HTTP_200_OK)



class ManagerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        managers = User.objects.all().filter(groups__name='Manager')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        if not user:
            return Response({'status': f"user with username = '{request.data['username']}' not found"}, status.HTTP_404_NOT_FOUND)
        new_manager = user
        managers = Group.objects.get(name='Manager')
        if new_manager.groups.filter(name='Manager').exists():
           return Response({'status': f"'{new_manager.username}' is already in manager group"}, status.HTTP_200_OK)
        managers.user_set.add(new_manager)
        return Response({'status': f"'{new_manager.username}' was added to manager group"}, status.HTTP_200_OK)
    
    def delete(self, request):
        user = User.objects.get(username=request.data['username'])
        if not user:
            return Response({'status': f"user with username = '{request.data['username']}' not found"}, status.HTTP_404_NOT_FOUND)
        old_manager = user
        managers = Group.objects.get(name='Manager')
        if not old_manager.groups.filter(name='Manager').exists():
           return Response({'status': f"'{old_manager.username}' is not in manager group"}, status.HTTP_200_OK)
        managers.user_set.remove(old_manager)
        return Response({'status': f"'{old_manager.username}' was removed to manager group"}, status.HTTP_200_OK)

class DeliveryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        delivery_guys = User.objects.all().filter(groups__name='Delivery')
        serializer = UserSerializer(delivery_guys, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        if not user:
            return Response({'status': f"user with username = '{request.data['username']}' not found"}, status.HTTP_404_NOT_FOUND)
        new_delivery_guy = user
        delivery_guys = Group.objects.get(name='Delivery')
        if new_delivery_guy.groups.filter(name='Delivery').exists():
           return Response({'status': f"'{new_delivery_guy.username}' is already in delivery group"}, status.HTTP_200_OK)
        delivery_guys.user_set.add(new_delivery_guy)
        return Response({'status': f"'{new_delivery_guy.username}' was added to delivery group"}, status.HTTP_200_OK)
    
    def delete(self, request):
        user = User.objects.get(username=request.data['username'])
        if not user:
            return Response({'status': f"user with username = '{request.data['username']}' not found"}, status.HTTP_404_NOT_FOUND)
        old_delivery_guy = user
        delivery_guys = Group.objects.get(name='Delivery')
        if not old_delivery_guy.groups.filter(name='Delivery').exists():
           return Response({'status': f"'{old_delivery_guy.username}' is not in delivery group"}, status.HTTP_200_OK)
        delivery_guys.user_set.remove(old_delivery_guy)
        return Response({'status': f"'{old_delivery_guy.username}' was removed to delivery group"}, status.HTTP_200_OK)

class BookingView(APIView):
    permission_classes = [IsAuthenticated]
    
    #def get(self, request):
    #    bookings = Booking.objects.all()
    #    serializer = BookingSerializer(bookings, many=True)
    #    return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'successfully booked a table',
                             'data': serializer.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)

class SingleBookingView(APIView):
    pass

class Category2View(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'successfully added category',
                             'data': serializer.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)

class SingleCategoryView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, reqeuest, pk):
        get_object_or_404(Category, pk=pk).delete()
        return Response({'status': 'successfully deleted menuitem'}, status.HTTP_200_OK)

class MenuItemsView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        serialzer = MenuItemCreateSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response({'status': 'successfully added menuitem',
                             'data': serialzer.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)
            
class SingleMenuView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'successfully replaced menuitem',
                             'data': serializer.data}, status.HTTP_200_OK)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'successfully modified menuitem',
                             'data': serializer.data}, status.HTTP_200_OK)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        get_object_or_404(MenuItem, pk=pk).delete()
        return Response({'status': 'successfully deleted menuitem'}, status.HTTP_200_OK)
    
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        carts = Cart.objects.filter(user=user_id)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
        
    def post(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        menuitem_id = MenuItem.objects.get(title=request.data['menuitem']).pk
        quantity = int(request.data['quantity'])
        unit_price = MenuItem.objects.get(pk=menuitem_id).price
        price = quantity * unit_price
        cart_item = {
            'user': user_id,
            'menuitem': menuitem_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'price': price
        }
        serializer = CartCreateSerializer(data=cart_item)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'successfully added cartitem',
                             'data': serializer.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        carts = Cart.objects.filter(user=user_id)
        num_carts = len(carts)
        if num_carts == 0:
            return Response({'status': 'no cartitems in cart'}, status.HTTP_200_OK)
        carts.delete()
        return Response({'status': f'successfully deleted {num_carts} cartitems from cart'}, status.HTTP_200_OK)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        if request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        
        elif request.user.groups.filter(name='Delivery').exists():
            orders = Order.objects.filter(delivery_crew=user_id)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        
        else:
            orders = Order.objects.filter(user=user_id)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

    
    def post(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        
        if Cart.objects.filter(user=user_id).count() < 1:
            return Response({'status': 'no items in cart'}, status.HTTP_200_OK)
        orderitems_info = Cart.objects.filter(user=user_id).values('menuitem', 'quantity', 'unit_price', 'price')
        order = {'user': user_id,
                 'total': orderitems_info.aggregate(total=Sum('price'))['total'],
                 'date': datetime.date.today()}
        serializer_order = OrderCreateSerializer(data=order)
        if serializer_order.is_valid():
            serializer_order.save()
            for orderitem_info in orderitems_info:
                orderitem = {'order': serializer_order.data['id'],
                             'menuitem': orderitem_info['menuitem'],
                             'quantity': orderitem_info['quantity'],
                             'unit_price': orderitem_info['unit_price'],
                             'price': orderitem_info['price']}
                serializer_orderitem = OrderItemCreateSerialzer(data=orderitem)
                if serializer_orderitem.is_valid():
                    serializer_orderitem.save()
            Cart.objects.filter(user=user_id).delete()
            return Response({'status': 'successfully created order from cartitems',
                             'data': serializer_order.data}, status.HTTP_201_CREATED)
        return Response({'status': 'unable to create order from cartitems'}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = Token.objects.get(key=request.auth.key).user_id
        orders = Order.objects.filter(user=user_id)
        num_orders= len(orders)
        if num_orders == 0:
            return Response({'status': 'no orders'}, status.HTTP_200_OK)
        orders.delete()
        return Response({'status': f'successfully delete {num_orders} orders'}, status.HTTP_200_OK)
        
class SingleOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if request.user != order.user and not request.user.groups.filter(name='Manager').exists():
            return Response({'status': 'not your order or no manager privileges'}, status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def patch(self, request, pk):   
        if request.user.groups.filter(name='Manager').exists():
            for k in request.data.keys():
                if k not in ['delivery_crew', 'status']:
                    return Response({'status': 'manager can only assign delivery-crew or change status'}, status.HTTP_403_FORBIDDEN)
                delivery_crew = User.objects.get(pk=request.data.get('delivery_crew'))
                if not delivery_crew:
                    return Response({'status': 'user does not exist'}, status.HTTP_400_BAD_REQUEST)
                if k == 'delivery_crew' and not delivery_crew.groups.filter(name='Delivery').exists():
                    return Response({'status': 'selected user is not in delivery-crew'}, status.HTTP_403_FORBIDDEN)
                if delivery_crew == Order.objects.get(pk=pk).delivery_crew:
                    return Response({'status': 'selected user is already delivery-crew'}, status.HTTP_200_OK)
                if k == 'status' and not request.data.get('status') in ['0', '1']:
                    return Response({'status': 'status can only be set to 0 (not delivered) and 1 (delivered)'}, status.HTTP_403_FORBIDDEN)    
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'successfully modified order',
                                 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'status': 'order modification failed'}, status.HTTP_400_BAD_REQUEST)
            
        if request.user.groups.filter(name='Delivery').exists():
            for k in request.data.keys():
                if k != 'status':
                    return Response({'status': 'delivery-crew can only change the status'}, status.HTTP_403_FORBIDDEN)
                if request.data.get('status') not in ['0', '1']:
                    return Response({'status': 'status can only be set to 0 (not delivered) and 1 (delivered)'}, status.HTTP_403_FORBIDDEN)         
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'successfully changed status of order',
                                 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'status': 'order modification failed'}, status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'status': 'only managers and delivery_crew can modify orders'}, status.HTTP_403_FORBIDDEN)
         
    
    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if request.user != order.user and not request.user.groups.filter(name='Manager').exists():
            return Response({'status': 'not your order or no manager privileges'}, status.HTTP_403_FORBIDDEN)
        order.delete()
        return Response({'status': 'successfully delete order'}, status.HTTP_200_OK)