from django.urls import path
from .views import *

urlpatterns = [
    path('me', user_me, name='user_me'),
    path('verify-email', verify_email, name='verify_email'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
    # path('profile/', profile, name='profile'),
]