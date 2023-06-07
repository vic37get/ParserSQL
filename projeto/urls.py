from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('parserSQL.urls')),
    path('admin/', admin.site.urls),
    
]
