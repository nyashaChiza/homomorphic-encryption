from django.urls import include, path
from django.contrib.auth import views as auth_views
from medical import views



urlpatterns = [
    path('tests', views.TestListView.as_view() , name='test_index'),
    path('tests/create', views.TestCreateView.as_view() , name='test_create'),
    path('tests/results/<int:pk>', views.TestResultsView.as_view() , name='test_add_results'),
    path('tests/details/<int:pk>', views.TestDetailView.as_view() , name='test_details'),
    path('patient/tests/<int:pk>', views.PatientTestsView.as_view() , name='patient_tests'),
    path('patient/treaments/<int:pk>', views.PatientTreatmentsView.as_view() , name='patient_treatments'),

    path('treatments', views.TreatmentListView.as_view() , name='treatment_index'),
    path('treatments/create', views.TestCreateView.as_view() , name='treatment_create'),
    path('treatments/details/<int:pk>', views.TreatmentDetailView.as_view() , name='treatment_details'),
    path('patients', views.PatientstListView.as_view() , name='patient_index'),

]
