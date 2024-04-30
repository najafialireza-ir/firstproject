from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(),  name='user_profile'),
    path('post/<int:post_id>/', views.UserPostDetailView.as_view(), name='post_detail'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('reply/<int:post_id>/<int:comment_id>/', views.NestedCommentReply.as_view(), name='nested_reply'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like')
    
]