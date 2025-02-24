from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import Order, OrderItem, OrderStatusHistory, Payment, ShippingAddress, Refund
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderStatusHistorySerializer,
    PaymentSerializer,
    ShippingAddressSerializer,
    RefundSerializer,
)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class OrderStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderStatusHistory.objects.all()
    serializer_class = OrderStatusHistorySerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
