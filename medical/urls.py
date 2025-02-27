from django.urls import include, path
from django.contrib.auth import views as auth_views
from medical import views



urlpatterns = [
    path('tests', views.TestListView.as_view() , name='test_index'),
    path('tests/create', views.TestCreateView.as_view() , name='test_create'),
    path('patient/create', views.PatientCreateView.as_view() , name='patient_create'),
    path('tests/results/<int:pk>', views.TestResultsView.as_view() , name='test_add_results'),
    path('tests/details/<int:pk>', views.TestDetailView.as_view() , name='test_details'),
    path('test/update/<int:pk>', views.TestUpdateView.as_view() , name='test_update'),
    path('patient/tests/<int:pk>', views.PatientTestsView.as_view() , name='patient_tests'),
    path('patient/treaments/<int:pk>', views.PatientTreatmentsView.as_view() , name='patient_treatments'),
    path('treatments', views.TreatmentListView.as_view() , name='treatment_index'),
    path('treatments/create', views.create_treatment , name='treatment_create'),
    path('treatments/details/<int:pk>', views.TreatmentDetailView.as_view() , name='treatment_details'),
    path('treatment/update/<int:pk>', views.TreatmentUpdateView.as_view() , name='treatment_update'),
    path('patients', views.PatientstListView.as_view() , name='patient_index'),
    path('medicine', views.MedicineListView.as_view() , name='medicine_index'),
    path('medicine/only/', views.MedicineListOnlyView.as_view() , name='medicine_only_index'),
    path('medicine/create', views.MedicineCreateView.as_view() , name='medicine_create'),
    path('medicine/update/<int:pk>', views.MedicineUpdateView.as_view() , name='medicine_update'),
    path('medications/delete/<int:pk>/', views.medication_delete_view, name='medicine_delete'),
    path('stats/index/', views.StatsIndexView.as_view(), name='stats_index'),
]