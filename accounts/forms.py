
from django import forms
from accounts.models import Profile

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