# Vendor Management System with Performance Metrics

This Vendor Management System is built using Django and Django REST Framework. It includes features such as vendor profile management, purchase order tracking, and vendor performance evaluation.

## Table of Contents

- [File Structure](#file-structure)
- [Features](#features)
- [Data Models](#data-models)
- [Backend Logic](#backend-logic)
- [API Endpoint Implementation](#api-endpoint-implementation)
- [Technical Considerations](#technical-considerations)

## File Structure

The important files and directories in the repository are as follows:

- `manage.py`: The Django project's management script.
- `care/`: The Django project directory.
- `settings.py`: The project's settings file.
- `urls.py`: The project's URL configuration.
- `wsgi.py`: The WSGI application entry point.
- `app/`: The Django app directory.
- `views.py`: Contains the views and their corresponding functions.
- `forms.py`: Contains the forms used in the app.
- `models.py`: Contains the database models used in the app.
- `templates/`: Contains the HTML templates used for rendering the views.
- `static/`: Contains static files such as CSS, JavaScript, and images.

## Features

1. **Vendor Profile Management:**
   - Create, list, retrieve, update, and delete vendors.

2. **Purchase Order Tracking:**
   - Create, list, retrieve, update, and delete purchase orders.
   - Filter purchase orders by vendor.

3. **Vendor Performance Evaluation:**
   - Calculate and display metrics for on-time delivery rate, quality rating average, average response time, and fulfillment rate.
   - Retrieve performance metrics for a specific vendor.

## Data Models

1. **Vendor Model:**
   - Fields: name, contact_details, address, vendor_code, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate.

2. **Purchase Order Model:**
   - Fields: po_number, vendor, order_date, delivery_date, items, quantity, status, quality_rating, issue_date, acknowledgment_date.

3. **Historical Performance Model:**
   - Fields: vendor, date, on_time_delivery_rate, quality_rating_avg, average_response_time, fulfillment_rate.

## Backend Logic

- **On-Time Delivery Rate:**
  - Calculated each time a PO status changes to 'completed'.
  - Logic: Count the number of completed POs delivered on or before delivery_date and divide by the total number of completed POs for that vendor.
 
```
  def completed_on_time_delivery_rate(self):
        completed_POs = self.purchaseorder_set.filter(status="completed", delivery_date__lte=timezone.now())
        total_comp_POs = completed_POs.count()

        if total_comp_POs > 0:
            on_time_delivery_rate = (total_comp_POs / float(self.purchaseorder_set.filter(status="completed").count())) * 100
            self.on_time_delivery_rate = round(on_time_delivery_rate, 2)
        else:
            self.on_time_delivery_rate = 0
```

- **Quality Rating Average:**
  - Updated upon the completion of each PO where a quality_rating is provided.
  - Logic: Calculate the average of all quality_rating values for completed POs of the vendor.
 
```
  def calculate_quality_rating_avg(self):
        quality_rating_all = self.purchaseorder_set.filter(status="completed", quality_rating__isnull=False)
        if quality_rating_all.exists():
            quality_rating_avg = quality_rating_all.aggregate(Avg('quality_rating'))["quality_rating__avg"]
            self.quality_rating_avg = round(quality_rating_avg, 2) if quality_rating_avg is not None else 0
        else:
            self.quality_rating_avg = 0
```

- **Average Response Time:**
  - Calculated each time a PO is acknowledged by the vendor.
  - Logic: Compute the time difference between issue_date and acknowledgment_date for each PO, and then find the average of these times for all POs of the vendor.
 
```
  def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(status='acknowledged', acknowledgment_date__isnull=False)

        if acknowledged_pos.exists():
            response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]
            average_response_time = sum(response_times) / acknowledged_pos.count()
            self.average_response_time = round(average_response_time / 60, 2)  
        else:
            self.average_response_time = 0
```

- **Fulfillment Rate:**
  - Calculated upon any change in PO status.
  - Logic: Divide the number of successfully fulfilled POs (status 'completed' without issues) by the total number of POs issued to the vendor.
 
```
  def calculate_fulfillment_rate(self):
        all_pos = self.purchaseorder_set.all()
        total_pos = all_pos.count()

        if total_pos > 0:
            successfully_fulfilled_pos = all_pos.filter(status='completed')
            fulfillment_rate = (successfully_fulfilled_pos.count() / float(total_pos)) * 100
            self.fulfillment_rate = round(fulfillment_rate, 2)
        else:
            self.fulfillment_rate = 0
```

## API Endpoint Implementation

- **Vendor Performance Endpoint (`GET /api/vendors/{vendor_id}/performance`):**
  - Retrieves the calculated performance metrics for a specific vendor.

- **Update Acknowledgment Endpoint (`POST /api/purchase_orders/{po_id}/acknowledge`):**
  - Updates acknowledgment_date and triggers the recalculation of average_response_time.

## Technical Considerations

- **Efficient Calculation:**
  - Ensured that the logic for calculating metrics is optimized to handle large datasets without significant performance issues.

- **Real-time Updates:**
  - Use of Django signals to trigger metric updates in real-time when related PO data is modified.


