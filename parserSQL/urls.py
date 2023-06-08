from django.urls import path
from . import views

app_name = 'parserSQL'
urlpatterns = [
    path('', views.index, name='index'),
    path('save/', views.save_text_file, name='save_text_file'),
    path('inicia_parser/', views.save_text_file, name='inicia_parser'),
]