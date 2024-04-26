from django.shortcuts import render, redirect
from django.views import View
from .form import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout



class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = "account/register.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, "User Register Successfully!", 'success')
            return redirect('home:home')
        return render(request, self.template_name,{'form':form})
    
    
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd =  form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in')
                if self.next:
                    return redirect(self.next)
            messages.error(request, 'username or password is wrong!')
        return render(request, self.template_name, {'form':form})
    
    
class UserLogoutView(LoginRequiredMixin, View):
    """dosen`t need dispatch due to loginRequiredMixin used 
    but you can use of (is not is_authenticated) with dispatch but LRM optimize.
    """
    def get(self, request):
        logout(request)
        messages.success(request, 'You logout', 'success')
        return render(request, 'homepage/home.html')
    
    
    
