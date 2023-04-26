from django.urls import path
from . import views
 

urlpatterns = [
    # check for authentication
    path('auth/', views.AuthorizationView.as_view(), name='check_authorization'),

    # render pages
    path('', views.RenderHomeView.as_view(), name='home'),
    path('about/', views.RenderAboutView.as_view(), name='about'),
    path('menu/', views.RenderMenuView.as_view(), name='render_menu'),
    path('menu/<slug:category>', views.RenderCategoryView.as_view(), name='render_category'),
    path('menu/<int:pk>/', views.RenderSingleMenuItemView.as_view(), name='render_menuitem'),
    path('book/', views.RenderBookView.as_view(), name='book'),
    
    # SignUp, Login, Logout, ProfilePage
    path('signupform/', views.RenderSignupFormView.as_view(), name='signupform'),
    path('loginform/', views.RenderLoginFormView.as_view(), name='loginform'),
    path('token/login/', views.LoginView.as_view(), name='token_create'),
    path('token/logout/', views.LogoutView.as_view(), name='token_destroy'),
    path('userprofile/', views.ProfileInformationView.as_view(), name='userprofile'),
    path('reservationsprofile/', views.ProfileReservationsInformationView.as_view(), name='reservations_profile'),
    path('profile/', views.RenderProfilePageView.as_view(), name='profile'),

    # raw data APIs
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('booking/<str:username>', views.SingleBookingView.as_view(), name='single_booking'),
    path('category/', views.CategoryView.as_view(), name='categories'),
    path('category/<str:category>', views.SingleCategoryView.as_view(), name='single_category'),
    path('menuitem/', views.MenuItemView.as_view(), name='menuitem'),
    path('menuitem/<int:pk>', views.SingleMenuView.as_view()),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('cartAPI/', views.ManualCartAPIView.as_view()),

    path('order/', views.OrderView.as_view(), name='order'),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
    
    
    
    path('manager/', views.ManagerView.as_view()),
    path('delivery/', views.DeliveryView.as_view()),
]