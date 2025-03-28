from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.contrib import messages
from accounts.forms import ProfileForm, UserForm
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from medical.forms import CustomPasswordChangeForm


# Reference the User model in a dynamic manner
User = get_user_model()


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password has been successfully updated.")
            request.user.changed_password = True
            request.user.save()
            return redirect("dashboard")  # Change this to your preferred redirect URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "account/change_password.html", {"form": form})


# View for logging out a user
def custom_logout(request):
    logout(request)
    return redirect(reverse('account_login'))


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
    
    def get_form(self):
        form = super().get_form()
        form.fields['user'].choices = [(self.request.user.pk, self.request.user)]
        return form



# View to create a new user profile
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile_create.html'
    context_object_name = 'profile'

    def get_success_url(self) -> str:
        return reverse('account_detail', kwargs={'pk': self.request.user.pk})
    
    def get_form(self):
        form = super().get_form()
        form.fields['user'].choices = [(self.request.user.pk, self.request.user)]
        return form


# View to create a new user account
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm  # Custom form for user creation
    template_name = 'users/create.html'
    success_url = reverse_lazy('users_index')

    def form_valid(self, form):
        # Optionally, handle additional actions after creating a user, such as sending a welcome email.
        return super().form_valid(form)


# View to create a new user account
class AccountSignUpView(CreateView):
    model = User
    form_class = UserForm  # Custom form for user creation
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account_login')

    def form_valid(self, form):
        # Optionally, handle additional actions after creating a user, such as sending a welcome email
        return super().form_valid(form)


# View to update an existing user account
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')

    def get_object(self, queryset=None):
        # Optionally, limit to certain users if required
        return get_object_or_404(User, pk=self.kwargs.get('pk'))
    
# View to update an existing user account
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail.html'



def user_delete_view(request, pk):
    User.objects.get(pk=pk).delete()
    messages.success(request, 'User deleted successfully!')

    return redirect(reverse('users_index'))