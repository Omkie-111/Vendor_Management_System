from django.urls import path
from .views import VendorCreateAPIView, VendorRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('', VendorCreateAPIView.as_view(), name = "vendor-list-create"),
    path('<int:pk>/', VendorRetrieveUpdateDeleteAPIView.as_view(), name = "vendor-list-update")
]