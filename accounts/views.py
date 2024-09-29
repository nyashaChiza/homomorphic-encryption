from django.forms import BaseModelForm
from accounts.forms import *
from django.views.generic import DetailView, UpdateView, CreateView
from accounts.models import User, Profile
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

def custom_logout(request):
    logout(request)
    return redirect(reverse('accounts_login'))


class AccountDetailView(DetailView):
    model = User
    template_name = 'account/detail.html'
    context_object_name = 'user'


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/update.html'
    context_object_name = 'profile'
    
    def get_success_url(self) -> str:
        return reverse('account_detail', kwargs={'pk':self.request.user.pk})

class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile_create.html'
    context_object_name = 'profile'

    def get_success_url(self) -> str:
        return reverse('account_detail', kwargs={'pk':self.request.user.pk})

