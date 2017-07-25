from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from django.views.generic.edit import CreateView, DeleteView
from message.forms import RegisterForm, MessageForm
from message.models import Message, Follow, Like


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = '/login'


class MessageView(CreateView):
    form_class = MessageForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return redirect(self.get_success_url())


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
    context_object_name = 'messages'

    def get_queryset(self):
        messages = Message.objects.all().order_by('-created')
        if self.request.user.is_authenticated():
            for message in messages:
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
        return messages


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = User
    context_object_name = 'current_user'
    login_url = 'login'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(
            user=User.objects.filter(username=self.kwargs['slug'])[0]).order_by('-created')
        context['following'] = len(Follow.objects.filter(following_user=context['current_user']))
        context['followers'] = len(Follow.objects.filter(followed_user=context['current_user']))
        context['messages_number'] = len(context['messages'])
        context['followed'] = Follow.objects.filter(following_user=self.request.user).filter(
            followed_user=context['current_user'])

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
