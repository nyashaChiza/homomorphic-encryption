from django.urls import path, include
from dashboard.views import DashboardView, AgeDashboardView, GenderDashboardView, LocationDashboardView, MedicationDashboardView, MedicationDataDownloadView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('research/age', AgeDashboardView.as_view(), name='age_dashboard'),
    path('research/gender', GenderDashboardView.as_view(), name='gender_dashboard'),
    path('research/location', LocationDashboardView.as_view(), name='location_dashboard'),
    path('research/medication', MedicationDashboardView.as_view(), name='medication_dashboard'),
    path('research/dataset/download', MedicationDataDownloadView.as_view(), name='dataset_download'),
]


