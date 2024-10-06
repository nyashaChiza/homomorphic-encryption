
from django import forms
from approval.models import Approval

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = "__all__"
        

    def __init__(self,  *args, **kwargs):
        super(ApprovalForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"