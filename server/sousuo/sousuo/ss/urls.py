from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('sousuo', views.sousuo),
    path('search', views.search, name='search'),
]
