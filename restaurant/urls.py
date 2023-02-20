from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('manager/', views.ManagerView.as_view()),
    path('delivery/', views.DeliveryView.as_view()),
    path('booking/', views.BookingView.as_view()),
    path('booking/<int:pk>', views.SingleBookingView.as_view()),
    path('menu/', views.MenuItemView.as_view()),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('order/', views.OrderView.as_view()),
]