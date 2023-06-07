from django.urls import path
from . import views

app_name = 'parserSQL'
urlpatterns = [
    path('', views.index, name='index'),
]