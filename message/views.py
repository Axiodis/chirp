from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect, render_to_response, render
from django.views.generic import ListView, DetailView

from django.views.generic.edit import CreateView, DeleteView
from message.forms import RegisterForm, MessageForm
from message.models import Message, Follow, Like


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/login'


def new_chirp(request):
    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES or None)
        if form.is_valid():
            chirp = form.save(commit=False)
            chirp.user_id = request.user.id
            chirp.save()
        else:
            messages.error(request, form.errors)
    return redirect(request.META.get('HTTP_REFERER'))


class FollowView(CreateView):
    def get(self, request, *args, **kwargs):
        followed_user = User.objects.filter(id=kwargs['id'])[0]
        f = Follow(following_user=request.user, followed_user=followed_user)
        f.save()
        return redirect('profile', slug=followed_user.username)


class UnfollowView(DeleteView):
    def get(self, request, *args, **kwargs):
        followed_user = User.objects.filter(id=kwargs['id'])[0]
        f = Follow.objects.filter(following_user=self.request.user).filter(followed_user=followed_user)
        f.delete()
        return redirect('profile', slug=followed_user.username)


class TimelineView(ListView):
    template_name = 'home.html'
    context_object_name = 'chirps'

    def get_queryset(self):
        chirps = Message.objects.all().order_by('-created')
        if self.request.user.is_authenticated():
            for chirp in chirps:
                chirp.liked = 0
                chirp.disliked = 0
                try:
                    like = chirp.like_set.get(user=self.request.user, message=chirp)
                    if like.like:
                        chirp.liked = 1
                    else:
                        chirp.disliked = 1
                except ObjectDoesNotExist:
                    pass
        return chirps


class ProfileBaseView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        context = super(ProfileBaseView, self).get_context_data(**kwargs)

        context["messages"] = Message.objects.filter(user=self.get_object()).order_by('-created')

        following = Follow.objects.filter(following_user=self.get_object())
        context["following"] = [f.followed_user for f in following]

        followers = Follow.objects.filter(followed_user=self.get_object())
        context["followers"] = [f.following_user for f in followers]

        for message in context['messages']:
            message.liked = 0
            message.disliked = 0
            try:
                like = message.like_set.get(user=self.request.user, message=message)
                if like.like:
                    message.liked = 1
                else:
                    message.disliked = 1
            except ObjectDoesNotExist:
                pass

        return context


class MyProfileView(ProfileBaseView):
    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(ProfileBaseView):
    def get_slug_field(self):
        return 'username'


class LikeView(View):
    def post(self, request, *args, **kwargs):

        message = Message.objects.get(id=request.POST['message_id'])
        try:
            like_dislike = Like.objects.get(message=message, user=self.request.user)
            if int(like_dislike.like) == int(request.POST['value']):
                like_dislike.delete()
            else:
                like_dislike.like = request.POST['value']
                like_dislike.save()
        except ObjectDoesNotExist:
            like_dislike = Like(user=self.request.user, message=message, like=request.POST['value'])
            like_dislike.save()
        return HttpResponse('')

