from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from django.views.generic.edit import CreateView, DeleteView
from message.forms import RegisterForm, MessageForm
from message.models import Message, Follow


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
        return Message.objects.all().order_by('-created')


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
        context['followed'] = Follow.objects.filter(following_user=self.request.user).filter(followed_user=context['current_user'])
        return context
