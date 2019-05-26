"""panamsquad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import views as core_views
from votes import urls as votes_urls
from opinions import urls as opinions_urls
from docs import urls as docs_urls
from infos import urls as infos_urls
from derby import urls as derby_urls
from events import urls as events_urls

admin.site.site_header = 'Panam Squad Administration'

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^privacy/$', core_views.privacy, name='privacy'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^votes/', include(votes_urls)),
    url(r'^opinions/', include(opinions_urls)),
    url(r'^docs/', include(docs_urls)),
    url(r'^profile/', include(infos_urls)),
    url(r'^derby/', include(derby_urls)),
    url(r'^events/', include(events_urls)),
]
