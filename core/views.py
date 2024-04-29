from rest_framework import viewsets
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models

from django.utils import timezone


def calculate_on_time_delivery_rate(vendor):
    """
    Calculate the on-time delivery rate for a given vendor.
    Returns The on-time delivery rate as a percentage. Returns 0 if there are no completed orders.
    """
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
    on_time_delivery_count = completed_orders.filter(
        delivery_date__lte=timezone.now()
    ).count()
    completed_orders_count = completed_orders.count()
    if completed_orders_count > 0:
        return (on_time_delivery_count / completed_orders_count) * 100
    return 0


def calculate_quality_rating_average(vendor):
    """
    Calculate the average quality rating for completed orders from a given vendor.
    Returns the average quality rating of completed orders from the vendor. If there are no completed orders with a quality rating,
    returns 0.
    """

    completed_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed", quality_rating__isnull=False
    )
    total_quality_rating = completed_orders.aggregate(
        total=models.Sum("quality_rating")
    )["total"]
    total_completed_orders = completed_orders.count()
    if total_completed_orders > 0:
        return total_quality_rating / total_completed_orders
    return 0


def calculate_average_response_time(vendor):
    """
    Calculates the average response time for completed orders from a given vendor.
    Returns the average response time in seconds. Returns 0 if there are no completed orders.
    """

    completed_orders = PurchaseOrder.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False
    )
    total_response_time = sum(
        (po.acknowledgment_date - po.issue_date).total_seconds()
        for po in completed_orders
    )
    total_completed_orders = completed_orders.count()
    if total_completed_orders > 0:
        return total_response_time / total_completed_orders
    return 0


def calculate_fulfillment_rate(vendor):
    """
    Calculate the fulfillment rate for a given vendor.
    Returns the fulfillment rate as a percentage. Returns 0 if there are no orders.
    """
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    successful_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status="completed"
    ).exclude(issue_date=None)
    if total_orders > 0:
        return (successful_orders.count() / total_orders) * 100
    return 0


class VendorList(APIView):
    def get(self, request, format=None):
        """
        Retrieves a list of all vendors from the database and serializes them using the VendorSerializer.

        Returns a response containing the serialized vendor data.
        """
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Handles the POST request to create a new vendor entry in the database
        Returns A response with the serialized vendor data if successful, or errors with status codes.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetail(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Get the details of a vendor.
        Returns a Response object containing the serialized vendor data.
        """

        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Update the details of a vendor based on the provided request data.
        Returns a response containing the updated vendor data if successful, or errors with status codes.
        """
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes the vendor based on the provided primary key.
        Returns A response object with status code HTTP_204_NO_CONTENT.
        """
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderList(APIView):
    def get(self, request, format=None):
        """
        Retrieves all purchase orders and serializes them using the PurchaseOrderSerializer.

        Returns serialized data of all purchase orders.
        """

        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Handles the POST request to create a new purchase order entry in the database.
        Returns a response with the serialized purchase order data if successful,
        or errors with status codes.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetail(APIView):
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Get the details of a purchase order.
        Returns the HTTP response containing the serialized purchase order data.
        """
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Update a purchase order with the given primary key
        Returns the HTTP response object containing the updated purchase order data if successful,or the errors if the
        purchase order serializer is invalid.
        """

        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes the purchase order based on the provided primary key.
        Returns a Response object with status code HTTP_204_NO_CONTENT.
        """
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoricalPerformanceList(APIView):
    def get(self, request, format=None):
        historical_performance = HistoricalPerformance.objects.all()
        serializer = HistoricalPerformanceSerializer(historical_performance, many=True)
        return Response(serializer.data)


class VendorPerformance(APIView):
    def get(self, request, vendor_id, format=None):
        vendor = Vendor.objects.get(pk=vendor_id)
        performance_data = {
            "on_time_delivery_rate": calculate_on_time_delivery_rate(vendor),
            "average_response_time": calculate_average_response_time(vendor),
            "fulfillment_rate": calculate_fulfillment_rate(vendor),
        }
        return Response(performance_data)


class PurchaseOrderAcknowledge(APIView):
    def post(self, request, po_id, format=None):
        """
        Records an acknowledgment for a purchase order.
        Returns a response object with a message indicating the success of the acknowledgment.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise Http404

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        vendor = purchase_order.vendor
        vendor.average_response_time = calculate_average_response_time(vendor)
        vendor.save()

        return Response({"message": "Acknowledgment recorded successfully"})
