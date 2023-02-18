from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Booking, MenuItem
from .serializers import BookingSerializer, MenuItemSerializer


def index(request):
    return render(request, 'index.html', {})


class BookingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'successfully booked a table',
                             'data': serializer.data})
        return Response({'status': 'failed'})


class SingleBookingView(APIView):
    pass

class CategoryView(APIView):
    pass

class SingleCategoryView(APIView):
    pass

class MenuItemView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serialzer = MenuItemSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response({'status': 'successfully added',
                             'data': serialzer.data})
            

class SingleMenuItemView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'successfully replaced',
                             'data': serializer.data})
    
    def patch(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'successfully modified',
                             'data': serializer.data})
    
    def delete(self, request, pk):
        get_object_or_404(MenuItem, pk=pk).delete()
        return Response({'status': 'successfully deleted'})