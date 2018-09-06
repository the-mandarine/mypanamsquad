from django.urls import path
from . import views

app_name = 'derby'
urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'presences', views.presences, name="presences"),
]

