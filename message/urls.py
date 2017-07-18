from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from message.views import RegisterView
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='index'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', auth_views.login,{'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'index'}, name='logout'),
]