from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg, F
from manager.models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_create(self, serializer):
        purchase_order = serializer.save()

        # Update vendor metrics when a new PO is created
        self.update_vendor_metrics(purchase_order.vendor)


class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_update(self, serializer):
        old_status = self.get_object().status
        purchase_order = serializer.save()

        # Update vendor metrics when a PO is updated (status changes)
        if old_status != purchase_order.status:
            self.update_vendor_metrics(purchase_order.vendor)

    def perform_destroy(self, instance):
        # Update vendor metrics when a PO is deleted
        vendor = instance.vendor
        instance.delete()
        self.update_vendor_metrics(vendor)

    # Acknowledge Purchase Order
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()

        # Update vendor metrics when acknowledgment_date is updated
        self.update_vendor_metrics(instance.vendor)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"Purchase Order ID: {instance.id}")

        # Acknowledge the purchase order by updating acknowledgment_date
        instance.acknowledgment_date = timezone.now()
        instance.save()
        print("Purchase Order acknowledged")

        # Trigger the recalculation of average_response_time
        instance.vendor.update_vendor_metrics()
        print("Vendor performance metrics updated")

        return Response({'message': 'Purchase Order acknowledged successfully.'}, status=status.HTTP_200_OK)