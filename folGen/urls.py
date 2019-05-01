
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('user/', include('user.urls')),
    path('timeline/', include('timeline.urls')),
]
