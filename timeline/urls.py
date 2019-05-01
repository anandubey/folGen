from django.urls import path
from . import views

# Timeline URL file
urlpatterns = [
    path('', views.index, name='timeline')
]
