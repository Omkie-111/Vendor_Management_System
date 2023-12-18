from django.urls import path
from .views import PurchaseOrderListCreateView, PurchaseOrderRetrieveUpdateDeleteView

urlpatterns = [
    path('', PurchaseOrderListCreateView.as_view(), name = "purchase-list-create"),
    path('<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name = "purchase-list-update")
]