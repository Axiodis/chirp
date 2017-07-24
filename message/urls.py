from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from message.views import RegisterView, MessageView, TimelineView, ProfileView, FollowView, UnfollowView, LikeView
from . import views

urlpatterns = [
    url(r'^$', TimelineView.as_view(), name='index'),
    url(r'^profile/(?P<slug>[-\w]+)/$', ProfileView.as_view(), name='profile'),
    url(r'^follow/(?P<id>[-\w]+)/$', FollowView.as_view(), name='follow'),
    url(r'^unfollow/(?P<id>[-\w]+)/$', UnfollowView.as_view(), name='unfollow'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^message/$', MessageView.as_view(), name='message'),
    url(r'^login/$', auth_views.login,{'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'index'}, name='logout'),
    url(r'^like/$', LikeView.as_view(), name='like'),

]