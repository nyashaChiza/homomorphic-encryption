from django.shortcuts import render
from approval.models import Approval
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from approval.forms import ApprovalForm

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView


class ApprovalListView(LoginRequiredMixin, ListView):
    model = Approval
    template_name = 'approval/index.html'
    context_object_name = 'approvals'


class ApprovalUpdateView(LoginRequiredMixin, UpdateView):
    model = Approval
    form_class = ApprovalForm
    template_name = 'approval/create.html'
    context_object_name = 'approval'
    success_url = reverse_lazy('approval_index')
    

class ApprovalDetaileView(LoginRequiredMixin, DetailView):
    model = Approval
    form_class = ApprovalForm
    template_name = 'approval/detail.html'
    context_object_name = 'approval'
    success_url = reverse_lazy('approval_index')
