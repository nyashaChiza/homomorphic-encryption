
from django import forms
from accounts.models import Profile, User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        
        widgets = {
            "dob": forms.widgets.DateInput(attrs={"type": "date"}),
        }

    def __init__(self,  *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model

# Use the custom user model if you have one
User = get_user_model()

class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password",
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password']
        widgets = {
            "password": forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Adding form-control class to all fields
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        # Custom validation for password confirmation
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Hash and set the password securely
        if commit:
            user.save()
        return user
