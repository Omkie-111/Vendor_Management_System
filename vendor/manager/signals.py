from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, Vendor, HistoricalPerformance

@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_on_po_completion(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.update_performance_metrics()

@receiver(pre_save, sender=PurchaseOrder)
def update_vendor_on_po_acknowledgment(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        instance.vendor.calculate_average_response_time()
        instance.vendor.save()

@receiver(post_save, sender=Vendor)
def create_historical_performance(sender, instance, created, **kwargs):
    """
    Signal receiver to create HistoricalPerformance when a Vendor is created.
    """
    if created:
        HistoricalPerformance.objects.create(
            vendor=instance,
            date=timezone.now(),
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )