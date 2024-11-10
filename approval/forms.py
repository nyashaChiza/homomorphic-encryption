
from django import forms
from approval.models import Approval

class ApprovalCreateForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = "__all__"
        exclude = ('status', 'viewed')
    
        widgets = {
            "doctor": forms.HiddenInput(),
        }

    def __init__(self,  *args, **kwargs):
        super(ApprovalCreateForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ApprovalUpdateForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = ("comment","status",)  # Include all fields from the model
        

    def __init__(self, *args, **kwargs):
        super(ApprovalUpdateForm, self).__init__(*args, **kwargs)
        
        # Add 'form-control' class to all fields
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        
       