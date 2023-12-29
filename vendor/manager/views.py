from rest_framework import generics

from .models import Vendor, HistoricalPerformance
from .serializers import VendorSerializer, HistoricalPerformanceSerializer

class VendorListCreateView(generics.ListCreateAPIView):
    """
    API View for listing and creating Vendor instances.
     """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View for retrieving, updating, and deleting a specific Vendor instance.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    """
    API View for retrieving Historical Performance data for a specific Vendor.
    """
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer