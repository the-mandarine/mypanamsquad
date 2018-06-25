from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path(r'', views.profile, name="profile"),
    path(r'success', views.success, name="success"),
    path(r'edit', views.edit, name="edit"),
    path(r'create', views.create, name="create"),
    path(r'<derby_number>', views.teammate, name="teammate"),
]

