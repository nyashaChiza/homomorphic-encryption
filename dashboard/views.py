from typing import Any
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from medical.models import Tests, Treatment, Medication
from approval.models import Approval
from accounts.models import User


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tests'] = Tests.objects.all()
        context['treatments'] = Treatment.objects.all()
        context['approval'] = Approval.objects.all()
        context['medicine'] = Medication.objects.all()
        context['users'] = User.objects.all()

        return context

    
