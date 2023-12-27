from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_on_po_completion(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.update_vendor_performance_metrics()

@receiver(pre_save, sender=PurchaseOrder)
def update_vendor_on_po_acknowledgment(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        instance.vendor.update_vendor_performance_metrics()
