
from django import forms
from medical.models import Treatment, Tests, Medication

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = "__all__"

        widgets = {
            "follow_up_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }

    def __init__(self,  *args, **kwargs):
        super(TreatmentForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class TestsForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = "__all__"
        
        widgets = {
            "follow_up_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }

    def __init__(self,  *args, **kwargs):
        super(TestsForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class TestResultsForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ('result', 'result_description',)
        

    def __init__(self,  *args, **kwargs):
        super(TestResultsForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = "__all__"
        

    def __init__(self,  *args, **kwargs):
        super(MedicineForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
