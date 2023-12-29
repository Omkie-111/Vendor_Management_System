from rest_framework import generics

from manager.models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    """
    API View for listing and creating Purchase Orders.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View for retrieving, updating, and deleting a specific Purchase Order.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class AcknowledgePurchaseOrderView(generics.RetrieveUpdateAPIView):
    """
    API View for acknowledging a specific Purchase Order.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
