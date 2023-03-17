from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/<slug:category>', views.CategoryView.as_view(), name='categories'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menuitem'),
    path('book/', views.BookView.as_view(), name='book'),
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('reservations/', views.ReservationsView.as_view(), name='reservations'),
    
    path('signupform/', views.SignupFormView.as_view(), name='signupform'),
    path('profile/', views.SingleUserView.as_view({'get': 'retrieve'}), name='profile'),
    #path('profile/<str:username>', views.SingleUserView.as_view({'get': 'retrieve'}), name='profile'),
    path('user-created/', views.UserCreateSuccessView.as_view()),
    path('loginform/', views.LoginFormView.as_view(), name='loginform'),
    #path('token/check-user/', views.CheckUserView.as_view(), name='check_user'),
    path('token/login/', views.LoginView.as_view(), name='token_create'),
    path('token/logout/', views.LogoutView.as_view(), name='token_destroy'),
    
    path('cart/', views.CartView.as_view(), name='cart'),
     
    path('manager/', views.ManagerView.as_view()),
    path('delivery/', views.DeliveryView.as_view()),
    path('booking/', views.BookingView.as_view()),
    path('booking/<int:pk>', views.SingleBookingView.as_view()),
    path('menuitem/', views.MenuItemsView.as_view()),
    path('menuitem/<int:pk>', views.SingleMenuView.as_view()),
    path('category/', views.Category2View.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('cartAPI/', views.CartAPIView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
]