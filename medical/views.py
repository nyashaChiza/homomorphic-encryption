from django.shortcuts import render
from medical.models import Tests, Treatment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from accounts.models import User
from medical.forms import TestsForm, TreatmentForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView


class TestListView(LoginRequiredMixin, ListView):
    model = Tests
    template_name = 'tests/index.html'
    context_object_name = 'tests'


class TestCreateView(LoginRequiredMixin, CreateView):
    model = Tests
    form_class = TestsForm
    template_name = 'tests/create.html'
    context_object_name = 'tests'
    success_url = reverse_lazy('test_index')
    
class TreatmentListView(LoginRequiredMixin, ListView):
    model = Treatment
    template_name = 'treatment/index.html'
    context_object_name = 'treatments'


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
