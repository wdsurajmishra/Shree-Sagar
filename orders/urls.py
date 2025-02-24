from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    OrderItemViewSet,
    OrderStatusHistoryViewSet,
    PaymentViewSet,
    ShippingAddressViewSet,
    RefundViewSet,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'order-status-history', OrderStatusHistoryViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'shipping-addresses', ShippingAddressViewSet)
router.register(r'refunds', RefundViewSet)

urlpatterns = router.urls
