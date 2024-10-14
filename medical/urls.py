from django.urls import include, path
from django.contrib.auth import views as auth_views
from medical import views



urlpatterns = [
    path('tests', views.TestListView.as_view() , name='test_index'),
    path('tests/create', views.TestCreateView.as_view() , name='test_create'),

    path('treatments', views.TreatmentListView.as_view() , name='treatment_index'),
    path('treatments/create', views.TestCreateView.as_view() , name='treatment_create'),

        path('patients', views.PatientstListView.as_view() , name='patient_index'),

]
