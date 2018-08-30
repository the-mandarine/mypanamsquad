from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'<slug>', views.detail, name="detail"),
    path(r'r/<slug>', views.redir, name="redir"),
]

