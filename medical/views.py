from django.shortcuts import render
from medical.models import Tests, Treatment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from accounts.models import User
from medical.forms import TestsForm, TreatmentForm, TestResultsForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView


class TestListView(LoginRequiredMixin, ListView):
    model = Tests
    template_name = 'tests/index.html'
    context_object_name = 'tests'

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

class TreatmentCreateView(LoginRequiredMixin, CreateView):
    model = Treatment
    form_class = TreatmentForm
    template_name = 'treatment/create.html'
    context_object_name = 'treatments'
    success_url = reverse_lazy('test_index')
    

class PatientstListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'patients/index.html'
    context_object_name = 'patients'
