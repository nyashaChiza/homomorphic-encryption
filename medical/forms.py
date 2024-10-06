
from django import forms
from medical.models import Treatment, Tests

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = "__all__"
        

    def __init__(self,  *args, **kwargs):
        super(TreatmentForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class TestsForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = "__all__"
        

    def __init__(self,  *args, **kwargs):
        super(TestsForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

