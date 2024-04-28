from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('reset', views.UserPasswordResetview.as_view(), name='reset_password'),
    path('reset/done', views.UserPasswordResetDoneView.as_view(), name='reset_done' ),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/complete', views.UserPasswordResetCompleteView.as_view(), name='reset_complete'),
    
]