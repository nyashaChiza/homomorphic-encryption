from django.urls import include, path
from django.contrib.auth import views as auth_views
from approval import views



urlpatterns = [
    path('', views.ApprovalListView.as_view() , name='approval_index'),
    path('approval/create', views.ApprovalCreateView.as_view() , name='approval_create'),
    path('approval/update/<int:pk>', views.ApprovalUpdateView.as_view() , name='approval_update'),
    path('approval/details/<uuid:uuid>', views.ApprovalDetailView.as_view() , name='approval_details'),

]
