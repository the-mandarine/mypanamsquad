from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path(r'', views.profile, name="profile"),
    path(r'edit', views.edit, name="edit"),
    path(r'baseedit', views.base_edit, name="base_edit"),
    path(r'<derby_number>', views.teammate, name="teammate"),
]

