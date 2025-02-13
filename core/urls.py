from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('optimus/', admin.site.urls),
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('medical/', include('medical.urls')),
    path('approval/', include('approval.urls')),
]
