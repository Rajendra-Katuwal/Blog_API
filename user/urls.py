from django.urls import path
from . import views

urlpatterns = [
    path('me', views.user_me, name='user_me'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    
    # path('logout/', views.logout, name='logout'),
    # path('profile/', views.profile, name='profile'),
]