from datetime import datetime
from django.contrib import messages
from typing import Any
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
