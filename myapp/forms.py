from django import forms
from django.contrib.auth.models import User

class EngineerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField()
   

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CustomerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField()
   

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
