
from django import forms
from django.forms import inlineformset_factory
from accounts.models import User
from medical.models import Treatment, Tests, Medication, TreatmentMedication


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['patient', 'doctor', 'title', 'treatment_type', 'status', 'description', 'symptoms', 'diagnosis', 'follow_up_date', 'notes']
        
        widgets = {
            "follow_up_date": forms.widgets.DateInput(attrs={"type": "date"}),
            # "medications": forms.widgets.SelectMultiple(attrs={"class": "form-select js-select2 select2-hidden-accessible"}),
        }

    def __init__(self, *args, **kwargs):
        super(TreatmentForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
                field.widget.attrs["class"] = "form-control"


class PatientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        
        widgets = {
            "follow_up_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
                field.widget.attrs["class"] = "form-control"

class TreatmentMedicationForm(forms.ModelForm):
    class Meta:
        model = TreatmentMedication
        fields = ['medication', 'method_of_administration', 'quantity', 'frequency']
   
    def __init__(self, *args, **kwargs):
        super(TreatmentMedicationForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            # Correctly checking field name
                field.widget.attrs["class"] = "form-control"

# Formset to manage multiple TreatmentMedication records
TreatmentMedicationFormSet = inlineformset_factory(
    Treatment,
    TreatmentMedication,
    form=TreatmentMedicationForm,
    extra=1,  # Number of blank forms initially displayed
    can_delete=True  # Allow users to remove medications
)


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
