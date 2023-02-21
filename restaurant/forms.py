from django import forms
#from django.contrib.auth.models import User

from .models import User, Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

class SignupForm(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        
class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'password']