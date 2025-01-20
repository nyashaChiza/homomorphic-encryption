from typing import Any
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from medical.models import Tests, Treatment, Medication
from approval.models import Approval
from accounts.models import User
from medical.helpers import MedicalDataAnalytics
import csv
from django.http import HttpResponse
from django.shortcuts import render



analytics = MedicalDataAnalytics()

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['treatments'] = Treatment.objects.all()
        context['approval'] = Approval.objects.all()
        context['medicine'] = Medication.objects.all()
        context['users'] = User.objects.all()

        return context

    
@method_decorator(login_required, name='dispatch')
class AgeDashboardView(TemplateView):
    template_name = 'research/age/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['test_age_donut'] = Tests.objects.all()
        context['treatment_age_donut_x'] = list(analytics.get_treatment_age_pie().keys())
        context['treatment_age_donut_y'] = list(analytics.get_treatment_age_pie().values())
        context['test_age_donut_x'] = list(analytics.get_test_age_pie().keys())
        context['test_age_donut_y'] = list(analytics.get_test_age_pie().values())
        context['treatment_type_age_bar_x'] = list(analytics.get_treatment_type_by_age_group().keys())
        context['treatment_type_age_bar_y'] = list(analytics.get_treatment_type_by_age_group().values())
        context['age_test_status_bar'] = Tests.objects.all()
        context['age_medicine_bar'] = Tests.objects.all()

        return context

@method_decorator(login_required, name='dispatch')
class LocationDashboardView(TemplateView):
    template_name = 'research/location/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['test_age_donut'] = Tests.objects.all()
        context['treatment_type_age_bar'] = Tests.objects.all()
        context['age_test_status_bar'] = Tests.objects.all()
        context['age_medicine_bar'] = Tests.objects.all()

        return context

@method_decorator(login_required, name='dispatch')
class GenderDashboardView(TemplateView):
    template_name = 'research/gender/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['test_age_donut'] = Tests.objects.all()
        context['treatment_gender_donut_x'] = list(analytics.get_treatment_gender_pie().keys())
        context['treatment_gender_donut_y'] = list(analytics.get_treatment_gender_pie().values())
        context['test_gender_donut_x'] = list(analytics.get_test_gender_pie().keys())
        context['test_gender_donut_y'] = list(analytics.get_test_gender_pie().values())
        context['treatment_type_gender_bar_x'] = list(analytics.get_treatment_by_gender().keys())
        context['treatment_type_gender_bar_y'] = list(analytics.get_treatment_by_gender().values())
        context['gender_test_status_bar'] = Tests.objects.all()
        context['gender_medicine_bar'] = Tests.objects.all()
        return context
    
@method_decorator(login_required, name='dispatch')
class MedicationDashboardView(TemplateView):
    template_name = 'research/medication/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['test_age_donut'] = Tests.objects.all()
        context['treatment_age_donut'] = Tests.objects.all()
        context['treatment_type_age_bar'] = Tests.objects.all()
        context['age_test_status_bar'] = Tests.objects.all()
        context['age_medicine_bar'] = Tests.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class MedicationDataDownloadView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        if kwargs.get('type'):
            dataset = analytics.get_research_dataset(kwargs.get('type'))
            # return csv file for download
        return super().get(request, *args, **kwargs)
    

def export_treatment_data(request, data_type=None):
    # Fetch dataset based on the given data_type
    dataset = analytics.get_dataset(data_type=f"{data_type}")
    if not dataset:
        return HttpResponse("No data available for the given type.", status=400)
    
    # Prepare the HttpResponse to serve CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{data_type}_treatment_data.csv"'
    
    writer = csv.DictWriter(response, fieldnames=dataset[0].keys())
    writer.writeheader()  # Write the header (keys)
    
    # Write the rows of the CSV
    for row in dataset:
        writer.writerow(row)
    
    return response
