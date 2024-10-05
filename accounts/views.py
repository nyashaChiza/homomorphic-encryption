from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from accounts.forms import ProfileForm, UserForm
from accounts.models import Profile

# Reference the User model in a dynamic manner
User = get_user_model()

# View for logging out a user
def custom_logout(request):
    logout(request)
    return redirect(reverse('accounts_login'))


# View to list all users
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    paginate_by = 10  # Adjust this number based on the size of your user list

    def get_queryset(self):
        # Customize the queryset if needed, for example, by filtering or ordering
        return User.objects.all().order_by('username')


# View to display the details of a user account
class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/detail.html'
    context_object_name = 'user'


# View to update an existing user profile
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/update.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Ensure the user can only update their own profile
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self) -> str:
        return reverse('account_detail', kwargs={'pk': self.request.user.pk})


# View to create a new user profile
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile_create.html'
    context_object_name = 'profile'

    def get_success_url(self) -> str:
        return reverse('account_detail', kwargs={'pk': self.request.user.pk})


# View to create a new user account
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm  # Custom form for user creation
    template_name = 'users/create.html'
    success_url = reverse_lazy('users_index')

    def form_valid(self, form):
        # Optionally, handle additional actions after creating a user, such as sending a welcome email.
        return super().form_valid(form)


# View to update an existing user account
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        # Optionally, limit to certain users if required
        return get_object_or_404(User, pk=self.kwargs.get('pk'))


# View to delete a user account
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        # Optionally, perform additional cleanup before deleting a user
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
