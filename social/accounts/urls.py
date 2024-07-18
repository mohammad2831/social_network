from django.urls import path
from . import views

app_name= 'accounts'
urlpatterns =[
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('profile/<str:username>', views.CreatePostView.as_view(), name='user_profile'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('comment/<slug:slug>', views.CreateCommentView.as_view(), name='create_comment'),    
    path('like/<slug:slug>', views.PostLikeView.as_view(), name='like_post'),    
    path('dislike/<slug:slug>', views.PostDislikeView.as_view(), name='dislike_post'),



    ]