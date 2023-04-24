from django.urls import path
from . import views
 

urlpatterns = [
    path('auth/', views.AuthorizationView.as_view(), name='check_authorization'),
    path('', views.RenderHomeView.as_view(), name='home'),
    path('about/', views.RenderAboutView.as_view(), name='about'),
    path('menu/', views.RenderMenuView.as_view(), name='menu'),
    path('menu/<slug:category>', views.RenderCategoryView.as_view(), name='categories'),
    path('menu/<int:pk>/', views.RenderSingleMenuItemView.as_view(), name='menuitem'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('book/', views.RenderBookView.as_view(), name='book'),
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    
    # SignUp, Login, Logout, ProfilePage
    path('signupform/', views.RenderSignupFormView.as_view(), name='signupform'),
    path('loginform/', views.RenderLoginFormView.as_view(), name='loginform'),
    path('token/login/', views.LoginView.as_view(), name='token_create'),
    path('token/logout/', views.LogoutView.as_view(), name='token_destroy'),
    path('userprofile/', views.ProfileInformationView.as_view(), name='userprofile'),
    path('reservationsprofile/', views.ProfileReservationsInformationView.as_view(), name='reservations_profile'),
    path('profile/', views.RenderProfilePageView.as_view(), name='profile'),

    path('booking/', views.BookingView.as_view()),
    path('booking/<int:pk>', views.SingleBookingView.as_view()), # TO DO
    path('cartAPI/', views.ManualCartAPIView.as_view()),

    
    
    path('menuitem/', views.MenuItemsView.as_view()),
    path('menuitem/<int:pk>', views.SingleMenuView.as_view()),
    path('category/', views.Category2View.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    
    
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
    
    path('manager/', views.ManagerView.as_view()),
    path('delivery/', views.DeliveryView.as_view()),
]