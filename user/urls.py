from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile, name='profile'),
    path('settings/', views.delete_user, name='settings'),
]
