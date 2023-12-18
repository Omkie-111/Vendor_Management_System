from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'