from django.urls import path

from .views import VendorListCreateView, VendorDetailView, VendorPerformanceView

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorDetailView.as_view(), name='vendor-list-update'),
    path('<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
]
