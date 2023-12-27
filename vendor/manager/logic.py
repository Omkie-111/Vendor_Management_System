from django.db.models import F, Avg
from django.utils import timezone
from .models import PurchaseOrder

def calculate_on_time_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
    return (on_time_orders.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

def calculate_quality_rating_avg(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    return completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

def calculate_average_response_time(vendor):
    acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    response_times = acknowledged_orders.exclude(issue_date__isnull=True).annotate(response_time=F('acknowledgment_date') - F('issue_date'))
    response_time_avg = response_times.aggregate(Avg('response_time'))['response_time__avg']

    return response_time_avg.total_seconds() if response_time_avg else 0.0
def calculate_fulfillment_rate(vendor):
    total_orders = PurchaseOrder.objects.filter(vendor=vendor)
    successful_orders = total_orders.filter(status='completed', quality_rating__isnull=True)
    return (successful_orders.count() / total_orders.count()) * 100 if total_orders.count() > 0 else 0

