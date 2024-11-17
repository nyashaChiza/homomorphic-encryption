from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.contrib import messages
from approval.models import Approval
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from approval.forms import ApprovalCreateForm, ApprovalUpdateForm

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView


class ApprovalListView(LoginRequiredMixin, ListView):
    model = Approval
    template_name = 'approval/index.html'
    context_object_name = 'approvals'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'Patient':
            context['approvals'] = self.request.user.doctors.all()

        elif self.request.user.role == 'Doctor':
            context['approvals'] = self.request.user.patients.all()

        else:
            context['approvals'] = Approval.objects.all()
        
        return context


class ApprovalCreateView(LoginRequiredMixin, CreateView):
    model = Approval
    form_class = ApprovalCreateForm
    template_name = 'approval/create.html'
    context_object_name = 'approval'
    success_url = reverse_lazy('approval_index')

    def get_initial(self):
        initial = super().get_initial()
        initial['doctor'] = self.request.user
        return initial
  


class ApprovalUpdateView(LoginRequiredMixin, UpdateView):
    model = Approval
    form_class = ApprovalUpdateForm
    template_name = 'approval/update.html'
    context_object_name = 'approval'
    success_url = reverse_lazy('approval_index')

    def form_valid(self, form):
        response = super().form_valid(form)

        object = self.get_object()
        object.viewed = False 
        object.save()
        messages.success(self.request, 'Approval updated successfully!')
        return response
    

class ApprovalDetailView(LoginRequiredMixin, DetailView):
    model = Approval
    form_class = ApprovalCreateForm
    template_name = 'approval/detail.html'
    context_object_name = 'approval'
    success_url = reverse_lazy('approval_index')
    lookup_field = 'uuid'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['object'].viewed = True
        context['object'].save()
        return context