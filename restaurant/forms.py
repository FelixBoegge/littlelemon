from django import forms
from .models import CustomUser, Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

class SignupForm(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        
class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'password']