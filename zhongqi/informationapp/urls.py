from django.contrib import admin
from django.urls import path, include

from informationapp import views
app_name='information'
urlpatterns = [
    path('homepage/',views.homepage,name='homepage'),
    path('bookinfo/',views.bookinfo,name='bookinfo'),
    path('bselect/',views.bselect,name='bselect'),
]