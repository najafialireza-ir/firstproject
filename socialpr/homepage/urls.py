from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(),  name='user_profile'),
    path('post/<int:post_id>/', views.UserPostDetailView.as_view(), name='post_detail'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('create/', views.PostCreateView.as_view(), name='post_create')
]