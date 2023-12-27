from django.urls import path
from .views import PurchaseOrderListCreateView, PurchaseOrderDetailView, AcknowledgePurchaseOrderView

urlpatterns = [
    path('', PurchaseOrderListCreateView.as_view(), name = "purchase-list-create"),
    path('<int:pk>/', PurchaseOrderDetailView.as_view(), name = "purchase-list-update"),
    path('<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]