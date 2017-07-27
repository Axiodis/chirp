from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from message.views import RegisterView, TimelineView, ProfileView, FollowView, UnfollowView, LikeView, \
    MyProfileView, new_chirp
from . import views

urlpatterns = [
    url(r'^$', TimelineView.as_view(), name='index'),
    url(r'^follow/(?P<id>[-\w]+)/$', login_required(FollowView.as_view()), name='follow'),
    url(r'^unfollow/(?P<id>[-\w]+)/$', login_required(UnfollowView.as_view()), name='unfollow'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^chirp/', login_required(new_chirp), name='chirp'),
    url(r'^login/$', auth_views.login,{'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'index'}, name='logout'),
    url(r'^like/$', LikeView.as_view(), name='like'),
    url(r'^my-profile/$', login_required(MyProfileView.as_view()), name='my-profile'),
    url(r'^profile/(?P<slug>[-\w]+)/$', login_required(ProfileView.as_view()), name='profile'),

]