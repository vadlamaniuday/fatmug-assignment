from django.urls import path
from . import views

urlpatterns = [
    path("api/vendors/", views.VendorList.as_view(), name="vendor-list"),
    path("api/vendors/<int:pk>/", views.VendorDetail.as_view(), name="vendor-detail"),
    path(
        "api/purchase_orders/",
        views.PurchaseOrderList.as_view(),
        name="purchaseorder-list",
    ),
    path(
        "api/purchase_orders/<int:pk>/",
        views.PurchaseOrderDetail.as_view(),
        name="purchaseorder-detail",
    ),
    path(
        "api/vendors/<int:vendor_id>/performance/",
        views.VendorPerformance.as_view(),
        name="vendor-performance",
    ),
    path(
        "api/purchase_orders/<int:po_id>/acknowledge/",
        views.PurchaseOrderAcknowledge.as_view(),
        name="purchaseorder-acknowledge",
    ),
]
