from django.urls import path
from . import views

app_name = 'opinions'

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'<slug>/', views.detail, name="detail"),
    path(r'<slug>/results', views.results, name="results"),
    path(r'<slug>/express', views.express, name="express"),
]

