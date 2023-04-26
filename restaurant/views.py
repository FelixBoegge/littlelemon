from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.views.generic.edit import FormView

from djoser.views import TokenCreateView, TokenDestroyView
from djoser.utils import login_user, logout_user
from djoser.conf import settings
from django.template.loader import render_to_string


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .models import Booking, Category, MenuItem, Cart, Order 
from .serializers import (CustomUserSerializer, UserCreateSerializer, 
                          BookingSerializer, CategorySerializer,
                          MenuItemSerializer, MenuItemCreateSerializer,
                          CartSerializer, CartCreateSerializer,
                          OrderItemCreateSerialzer,
                          OrderSerializer, OrderCreateSerializer)
from .forms import BookingForm, SignupForm, LoginForm

from datetime import datetime
import json

User = get_user_model()


# -------------------------------------------------render pages-----------------------------------------------------------
class AuthorizationView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            return HttpResponse({'user': user}, status.HTTP_200_OK)
        else:
            return HttpResponse(status.HTTP_401_UNAUTHORIZED)

class RenderHomeView(APIView):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            token = Token.objects.get(user=request.user.id).key
            context = {'Authentication': 'Token ' + token}
        return render(request, 'index.html', context)

class RenderAboutView(APIView):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            token = Token.objects.get(user=request.user.id).key
            context = {'Authentication': 'Token ' + token}
        return render(request, 'about.html', context)

class RenderMenuView(APIView):
    def post(self, request):
        context = json.loads(request.body)
        rendered_menu = render_to_string("menu.html", context)
        return HttpResponse(rendered_menu)
    
    def get(self, request):
        categories = Category.objects.all()
        #serialized_categories = CategorySerializer(categories, many=True)
        context = {'categories': categories}
        return render(request, 'menu.html', context)

class RenderCategoryView(APIView):
    def post(self, request):
        context = json.loads(request.body)
        rendered_category = render_to_string('category.html', context)
        return HttpResponse(rendered_category)
    
    def get(self, request, category):
        items = MenuItem.objects.all()
        if category:
            items = items.filter(category__slug=category)
        category_name = Category.objects.get(slug=category).title
        context = {'menuitems': items,
                   'category': category_name}
        return render(request, 'category.html', context)

class RenderSingleMenuItemView(APIView):
    def get(self, request, pk):
        if pk: 
            menuitem = MenuItem.objects.get(pk=pk) 
        else: 
            menuitem = "" 
        return render(request, 'menuitem.html', {"menuitem": menuitem}) 

class RenderBookView(APIView):
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
                user = User.objects.get(username=data['username']),
                name = data['username'],
                num_guests = data['num_guests'],
                booking_date = data['booking_date'],
                booking_slot = data['booking_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    def get(self, request):
        date = request.GET.get('date',datetime.today().date())
        bookings = Booking.objects.all().filter(booking_date=date)
        serialized_bookings = serializers.serialize('json', bookings)
        return HttpResponse(serialized_bookings, content_type='application/json')



# ---------------------------------------SignUp, Login, Logout, ProfilePage-------------------------------------------
class RenderSignupFormView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    def form_valid(self, form):
        return super().form_valid(form)

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
            new_user.save()
            return Response({'status': 'succesfully registered'}, status.HTTP_201_CREATED)
        else:
            return HttpResponse("{'error':1}", content_type='application/json')

class RenderLoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    def form_valid(self, form):
        return super().form_valid(form)

class LoginView(TokenCreateView):
    def _action(self, serializer):
        token = login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        user_id = Token.objects.get(key=token).user_id
        user = User.objects.get(id=user_id)
        response = HttpResponseRedirect(reverse('home'))
        response.set_cookie('authToken', token, secure=True, samesite='Lax')
        response.set_cookie('username', user.username, secure=True, samesite='Lax')
        response.set_cookie('firstName', user.first_name, secure=True, samesite='Lax')
        response.set_cookie('lastName', user.last_name, secure=True, samesite='Lax')
        response.set_cookie('email', user.email, secure=True, samesite='Lax')
        return response
       
class LogoutView(TokenDestroyView):
    def post(self, request):
        logout_user(request)
        response = HttpResponseRedirect(reverse('loginform'))
        response.delete_cookie('authToken')
        response.delete_cookie('username')
        response.delete_cookie('firstName')
        response.delete_cookie('lastName')
        response.delete_cookie('email')
        return response

class ProfileInformationView(APIView):
    def get(self, request):
        user = request.user
        serialized_user = CustomUserSerializer(user)
        context = serialized_user.data
        response = Response(context, status.HTTP_200_OK)
        return response
    
class ProfileReservationsInformationView(APIView):
    def get(self, request):
        reservations = Booking.objects.filter(user=request.user)
        serialized_reservations = BookingSerializer(reservations, many=True)
        context = serialized_reservations.data
        response = Response(context, status.HTTP_200_OK)
        return response
    
class RenderProfilePageView(APIView):
    def post(self, request):
        context = json.loads(request.body)
        rendered_profile = render_to_string("profile.html", context)
        return HttpResponse(rendered_profile)



# ----------------------------------Fetch and manipulate data----------------------------------------------
class BookingView(APIView):    
    def get(self, request):
        if not request.user == 'AnonymousUser':
            reservartions = Booking.objects.filter(user=request.user)
        else: 
            reservartions = Booking.objects.all()
        serialized_reserations = BookingSerializer(reservartions, many=True)
        return Response(serialized_reserations.data, status.HTTP_200_OK)
    
    def post(self, request):
        exist = Booking.objects.filter(booking_date=request.data['booking_date']).filter(
            booking_slot=request.data['booking_slot']).exists()
        if exist:
            return Response({'status': 'selected time slot at given date is already blocked'},
                            status.HTTP_200_OK)
        
        serialized_reseration = BookingSerializer(data=request.data)
        if serialized_reseration.is_valid():
            serialized_reseration.save(user=request.user)
            return Response({'status': 'successfully booked a table',
                             'data': serialized_reseration.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data',
                         'data': serialized_reseration.data}, status.HTTP_400_BAD_REQUEST)

class SingleBookingView(APIView):
    def delete(self, request, username):
        reservations_to_delete = Booking.objects.filter(name=username)
        if reservations_to_delete:
            num_reservations_to_delete = len(reservations_to_delete)
            reservations_to_delete.delete()
            return Response({'status': f"successfully deleted all ({num_reservations_to_delete}) reservations from '{username}'"},
                            status.HTTP_200_OK)
        else:
            return Response({'status': 'no reservations found for given user'},
                            status.HTTP_200_OK)

class CategoryView(APIView):    
    def get(self, request):
        categories = Category.objects.all()
        serialized_categories = CategorySerializer(categories, many=True)
        context = serialized_categories.data
        return Response(context, status.HTTP_200_OK)
    
    def post(self, request):
        serialized_category = CategorySerializer(data=request.data)
        if serialized_category.is_valid():
            serialized_category.save()
            return Response({'status': 'successfully added category',
                             'data': serialized_category.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data'}, status.HTTP_400_BAD_REQUEST)

class SingleCategoryView(APIView):    
    def get(self, request, category):
        category = get_object_or_404(Category, slug=category)
        serialized_category = CategorySerializer(category)
        context = serialized_category.data
        return Response(context, status.HTTP_200_OK)
    
    def delete(self, reqeuest, category):
        get_object_or_404(Category, slug=category).delete()
        return Response({'status': 'successfully deleted menuitem'}, status.HTTP_200_OK)

class MenuItemView(APIView):
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
   
class CartView(APIView):
    def get(self, request):
        carts = Cart.objects.filter(user=request.user)
        serialized_carts = CartSerializer(carts, many=True)
        context = serialized_carts.data
        response = Response(context, status.HTTP_200_OK)
        return response
    
    @csrf_exempt
    def post(self, request):
        data = json.load(request)
        user = request.user
        menuitem = MenuItem.objects.get(title=data['menuitem'])
        exist = Cart.objects.filter(user=user).filter(menuitem=menuitem).exists()
        if exist == False:
            quantity = int(data['num_items'])
            unit_price = MenuItem.objects.get(pk=menuitem.id).price
            price = quantity * unit_price
            cart_item = Cart(
                user = user,
                menuitem =  menuitem,
                quantity = quantity,
                unit_price = unit_price,
                price = price
            )
            cart_item.save()
            return HttpResponse(status.HTTP_200_OK)
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
        
    
    def delete(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        num_cart_items = len(cart_items)
        if num_cart_items == 0:
            return Response({'status': 'no cartitems in cart'}, status.HTTP_200_OK)
        cart_items.delete()
        return Response({'status': f'successfully deleted {num_cart_items} cartitems from cart'}, status.HTTP_200_OK)   
 
class ManualCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
        
    def post(self, request):
        menuitem_id = MenuItem.objects.get(title=request.data['menuitem']).pk
        
        exist = Cart.objects.filter(menuitem=menuitem_id).filter(user=request.user).exists()
        if exist:
            return Response({'status': f"{request.user.username} already has {request.data['menuitem']} in his/her cart"},
                            status.HTTP_200_OK)
        
        quantity = int(request.data['quantity'])
        unit_price = MenuItem.objects.get(pk=menuitem_id).price
        price = quantity * unit_price
        cart_item = {
            'user': request.user.id,
            'menuitem': menuitem_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'price': price
        }
        serialized_cartitem = CartCreateSerializer(data=cart_item)
        if serialized_cartitem.is_valid():
            serialized_cartitem.save()
            return Response({'status': 'successfully added cartitem',
                             'data': serialized_cartitem.data}, status.HTTP_201_CREATED)
        return Response({'status': 'provide valid data', 
                         'data': serialized_cartitem.data}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = User.objects.get(request.user).user_id
        cart_items = Cart.objects.filter(user=user_id)
        num_cart_items = len(cart_items)
        if num_cart_items == 0:
            return Response({'status': 'no cartitems in cart'}, status.HTTP_200_OK)
        cart_items.delete()
        return Response({'status': f'successfully deleted {num_cart_items} cartitems from cart'}, status.HTTP_200_OK)






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
    
class ManagerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        managers = User.objects.all().filter(groups__name='Manager')
        serializer = UserCreateSerializer(managers, many=True)
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
        serializer = UserCreateSerializer(delivery_guys, many=True)
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
