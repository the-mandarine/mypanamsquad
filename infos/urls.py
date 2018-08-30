from django.urls import path
from . import views

app_name = 'profile'
urlpatterns = [
    path(r'', views.profile, name="profile"),
    path(r'success', views.success, name="success"),
    path(r'edit', views.edit, name="edit"),
    path(r'membership', views.membership, name="membership"),
    path(r'create', views.create, name="create"),
    path(r'subscribe', views.subscribe, name="subscribe"),
    path(r'health_cert', views.health_cert_redir, name="health_cert_redir"),
    path(r'health_cert/<filename>', views.health_cert, name="health_cert"),
    path(r'<derby_number>', views.teammate, name="teammate"),
]

