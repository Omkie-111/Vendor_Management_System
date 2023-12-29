from rest_framework import serializers
from manager.models import PurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the PurchaseOrder model.
    """
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
