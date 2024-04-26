from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your Name'}))
    email = forms.EmailField(widget=forms.PasswordInput(attrs={'placeholder':'@gmail.com'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='confirm', widget=forms.PasswordInput())

    
    def clean_email(self):
        """Email Validation for not repeted and exists.
        """
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists!')
        return email
    
    
    
    def  clean(self):
        """validation two fields
        """
        cd = super().clean()  # use of cleand_data
        p1 = cd.get('password1',)
        p2 = cd.get('password2',)
        if p1 and p2 and p1 != p2:
            raise ValidationError('password doesn`t match')
    
    
    
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'placeholder':'YourName'}))
    password = forms.CharField(widget=forms.PasswordInput({'placeholder':'8-Char'}))