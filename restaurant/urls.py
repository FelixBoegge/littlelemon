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
    
    path('signupform/', views.SignupFormView.as_view(), name='signupform'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('loginform/', views.LoginFormView.as_view(), name='loginform'),
    #path('login/', views.LoginView.as_view(), name='login'),
    
    path('menu/<slug:category>', views.MenuItemView.as_view(), name='menuitems'),
     
    path('manager/', views.ManagerView.as_view(), name='manager'),
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('booking/<int:pk>', views.SingleBookingView.as_view(), name='single_booking'),
    path('menuitem/', views.MenuItemsView.as_view()),
    path('menuitem/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
]