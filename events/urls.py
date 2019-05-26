from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'<slug>/', views.detail, name="detail"),
    path(r'<slug>/attend', views.attend, name="attend"),
    path(r'<slug>/proxy', views.proxy, name="proxy"),
]

