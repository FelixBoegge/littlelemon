from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/<int:pk>/', views.SingleMenuView.as_view(), name='menu_item'),
    path('book/', views.BookView.as_view(), name='book'),
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('reservations/', views.ReservationsView.as_view(), name='reservations'),
    
    path('registration/', views.SignupView.as_view(), name='registration'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('login/', views.LoginView.as_view(), name='wow'),
    path('userlogin/', views.UserLoginView.as_view(), name='userlogin'),
     
    path('manager/', views.ManagerView.as_view(), name='manager'),
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('booking/<int:pk>', views.SingleBookingView.as_view(), name='single_booking'),
    path('menu/', views.MenuItemView.as_view()),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
]