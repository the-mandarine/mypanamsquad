from django.urls import path
from . import views

app_name = 'derby'
urlpatterns = [
    path(r'profile', views.profile, name="profile"),
    path(r'update_profile', views.profile_update, name="profile_update"),
    path(r'trainings', views.trainings, name="trainings"),
    path(r'training/<date>', views.training, name="training"),
    path(r'presences', views.presences, name="presences"),
]

