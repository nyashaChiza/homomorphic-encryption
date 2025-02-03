import datetime
from django.shortcuts import render
from medical.models import Tests, Treatment, Medication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from accounts.models import User, Approval
from django.contrib import messages 
from medical.helpers import get_treatments_with_medication
from medical.forms import TestsForm, TreatmentForm, TestResultsForm, MedicineForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import TreatmentForm, TreatmentMedicationFormSet
from accounts.forms import UserForm
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Medication, Treatment
from medical.helpers import MedicalCalculations

calculus = MedicalCalculations()

class TestListView(LoginRequiredMixin, ListView):
    model = Tests
    template_name = 'tests/index.html'
    context_object_name = 'tests'

class StatsIndexView(LoginRequiredMixin, ListView):
    model = Tests
    template_name = 'research/analytics/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['patients']= User.objects.filter(role='Patient')
        context['medication']= Medication.objects.all()
        context['treatment_types'] = [type_[0] for type_ in  Treatment.TREATMENT_TYPE_CHOICES]

        if self.request.GET.get('patient_id') and self.request.GET.get('medication_id'):
            context['medical_adherence'] = calculus.calculate_medication_adherence(self.request.GET.get('patient_id'), self.request.GET.get('medication_id'))
        
        if self.request.GET.get('treatment_type'):
            context['average_recovery_type'] = calculus.calculate_average_recovery_time(self.request.GET.get('treatment_type'))


        if self.request.GET.get('follow_up_date'):
            context['patients'] = calculus.find_high_risk_patients(self.request.GET.get('follow_up_date'))

        if self.request.GET.get('type'):
            context['treatment_success_rate'] = calculus.calculate_treatment_success_rate(self.request.GET.get('type'))

        if self.request.GET.get('treatment'):
            context['common_symptoms'] = calculus.get_common_symptoms_for_treatment(self.request.GET.get('treatment'))

        return context
        

class TestDetailView(DetailView):
    template_name = 'tests/detail.html'
    context_object_name = 'test'
    model = Tests

class PatientTestsView(DetailView):
    template_name = 'tests/tests.html'
    context_object_name = 'test'
    model = User

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        
        context['tests'] = kwargs.get('object').tests.all()
        return context

class PatientTreatmentsView(DetailView):
    template_name = 'treatment/treatments.html'
    context_object_name = 'treatment'
    model = User

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        
        context['treatments'] = kwargs.get('object').treatments.all()
        return context

class TestCreateView(LoginRequiredMixin, CreateView):
    model = Tests
    form_class = TestsForm
    template_name = 'tests/create.html'
    context_object_name = 'tests'
    success_url = reverse_lazy('test_index')

    def get_form(self) :
        form = super().get_form()
        if self.request.user.role in ['Doctor', 'Clerk']:
            patients = [('','---------')]
            doctors = [('','---------'), (self.request.user.pk,self.request.user)]
            patients.extend([(approval.patient.pk, approval.patient) for approval in self.request.user.patients.filter(status="Granted").all()])
        else:
            patients = [(self.request.user.pk,self.request.user)]
            doctors = [(patient.pk, patient) for patient in User.objects.filter(role='Doctor').all()]
            form.fields['doctor'].label = 'Doctor/ Clerk'
        
        form.fields['patient'].choices = patients
        form.fields['doctor'].choices = doctors

        return form
    
    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)

        # Add a success message
        messages.success(self.request, 'Test added successfully!')

        return response


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Tests
    form_class = UserForm
    template_name = 'patients/add_patient.html'
    context_object_name = 'tests'
    success_url = reverse_lazy('patient_index')

    def get_form(self) :
        form = super().get_form()
        roles = [('','---------'), ('Patient', 'Patient')]
        form.fields['role'].choices = roles

        return form
    
    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)


        # Add a success message
        patient = User.objects.last()
        doctor = self.request.user

        Approval.objects.create(patient=patient, doctor=doctor, status='Granted')
        messages.success(self.request, f'Patient added successfully!')

        return response


class TestResultsView(LoginRequiredMixin, UpdateView):
    model = Tests
    form_class = TestResultsForm
    template_name = 'tests/add_results.html'
    context_object_name = 'test'
    success_url = reverse_lazy('test_index')


class TreatmentListView(LoginRequiredMixin, ListView):
    model = Treatment
    template_name = 'treatment/index.html'
    context_object_name = 'treatments'


class TreatmentDetailView(DetailView):
    template_name = 'treatment/details.html'
    context_object_name = 'treatment'
    model = Treatment

def create_treatment(request):
    if request.method == "POST":
        treatment_form = TreatmentForm(request.POST)
        medication_formset = TreatmentMedicationFormSet(request.POST)

        # Dynamically set patient and doctor choices based on user role
        if request.user.role in ['Doctor', 'Clerk']:
            patients = [('','---------')]
            doctors = [('','---------'), (request.user.pk, request.user)]
            # Assuming `request.user.patients` is a reverse relation that gives all associated patients
            patients.extend([(approval.patient.pk, approval.patient) for approval in request.user.patients.filter(status="Granted").all()])
        else:
            patients = [(request.user.pk, request.user)]
            doctors = [(patient.pk, patient) for patient in User.objects.filter(role='Doctor').all()]

        # Set the choices dynamically for the form
        treatment_form.fields['patient'].choices = patients
        treatment_form.fields['doctor'].choices = doctors

        if treatment_form.is_valid() and medication_formset.is_valid():
            treatment = treatment_form.save()

            # Save each medication associated with the treatment
            medication_formset.instance = treatment
            medication_formset.save()

            messages.success(request, "Treatment and medications added successfully!")
            return redirect('treatment_list')  # Redirect to a list or detail view

    else:
        treatment_form = TreatmentForm()
        medication_formset = TreatmentMedicationFormSet()

        # Dynamically set patient and doctor choices for GET request
        if request.user.role in ['Doctor', 'Clerk']:
            patients = [('','---------')]
            doctors = [('','---------'), (request.user.pk, request.user)]
            patients.extend([(approval.patient.pk, approval.patient) for approval in request.user.patients.filter(status="Granted").all()])
        else:
            patients = [(request.user.pk, request.user)]
            doctors = [(patient.pk, patient) for patient in User.objects.filter(role='Doctor').all()]

        # Set the choices dynamically for the form
        treatment_form.fields['patient'].choices = patients
        treatment_form.fields['doctor'].choices = doctors

    context = {
        'treatment_form': treatment_form,
        'medication_formset': medication_formset,
    }
    return render(request, 'treatment/create.html', context)

class TreatmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = 'treatment/update.html'
    context_object_name = 'treatment'
    success_url = reverse_lazy('treatment_index')

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, 'Treatment updated successfully!')
        return response

    def get_form(self) :
        form = super().get_form()
        form.fields['doctor'].label = 'Doctor/ Clerk'
        return form
    

class TestUpdateView(LoginRequiredMixin, UpdateView):
    model = Tests
    form_class = TestsForm
    template_name = 'tests/update.html'
    context_object_name = 'test'
    success_url = reverse_lazy('test_index')

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, 'Test updated successfully!')
        return response
    
    def get_form(self) :
        form = super().get_form()
        form.fields['doctor'].label = 'Doctor/ Clerk'
        return form

class PatientstListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'patients/index.html'
    context_object_name = 'patients'


class MedicineListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'medicine/index.html'
    context_object_name = 'meds'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] =  get_treatments_with_medication()
        return context


class MedicineCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicineForm
    template_name = 'medicine/create.html'
    context_object_name = 'meds'
    success_url = reverse_lazy('medicine_index')

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)

        # Add a success message
        messages.success(self.request, 'Medicine added successfully!')
        return response
    
class MedicineUpdateView(LoginRequiredMixin, UpdateView):
    model = Medication
    form_class = MedicineForm
    template_name = 'medicine/update.html'
    context_object_name = 'medicine'
    success_url = reverse_lazy('medicine_index')

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the form
        response = super().form_valid(form)

        # Add a success message
        messages.success(self.request, 'Medicine updated successfully!')
        return response
    
def medication_delete_view(request, pk):
    Medication.objects.get(pk=pk).delete()
    messages.success(request, 'Medicine deleted successfully!')

    return redirect(reverse('medicine_index'))
 


