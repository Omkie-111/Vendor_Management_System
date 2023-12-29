from rest_framework import serializers

from .models import Vendor, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vendor model.
    """
    class Meta:
        model = Vendor
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the HistoricalPerformance model.
    """
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
