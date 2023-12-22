from django.db import models
from django.utils import timezone
from django.db.models import Count, Avg, F

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def completed_on_time_delivery_rate(self):
        completed_POs = self.purchaseorder_set.filter(status = "completed", delivery_date__lte = timezone.now())
        total_comp_POs = completed_POs.count()

        if total_comp_POs > 0:
            on_time_delivery_rate = (total_comp_POs / F('purchaseorder__count'))
            self.on_time_delivery_rate = round(on_time_delivery_rate,2)

        else:
            self.on_time_delivery_rate = 0

    def calculate_quality_rating_avg(self):
        quality_rating_all = self.purchaseorder_set.filter(status = "completed", quality_rating__isnull = False)
        if quality_rating_all.exists:
            quality_rating_avg = quality_rating_all.aggregate(Avg('quality_rating'))["quality_rating_avg"]
            self.quality_rating_avg = round(quality_rating_avg,2)
        else:
            self.quality_rating_avg = 0
    
    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(status='acknowledged', acknowledgment_date__isnull=False)

        if acknowledged_pos.exists():
            response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
            average_response_time = sum(response_times) / acknowledged_pos.count()
            self.average_response_time = round(average_response_time / 60, 2)  # Convert seconds to minutes
        else:
            self.average_response_time = 0

    def calculate_fulfillment_rate(self):
        all_pos = self.purchaseorder_set.all()
        total_pos = all_pos.count()

        if total_pos > 0:
            successfully_fulfilled_pos = all_pos.filter(status='completed', issues__isnull=True)
            fulfillment_rate = (successfully_fulfilled_pos.count() / F('purchaseorder__count')) * 100
            self.fulfillment_rate = round(fulfillment_rate, 2)
        else:
            self.fulfillment_rate = 0

    def update_performance_metrics(self):
        self.calculate_on_time_delivery_rate()
        self.calculate_quality_rating_avg()
        self.calculate_average_response_time()
        self.calculate_fulfillment_rate()
        self.save()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()