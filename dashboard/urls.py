from django.urls import path, include
from dashboard.views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')
]
