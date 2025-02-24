from django.db import models
from django.contrib.auth.models import User
from inventory.models import ProductVariant
import uuid
from accounts.models import Customer
from django.utils.translation import gettext_lazy as _



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shipping_addresses', verbose_name=_('Customer'))
    full_name = models.CharField(max_length=255, verbose_name=_('Full Name'))
    address_line_1 = models.CharField(max_length=255, verbose_name=_('Address Line 1'))
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Address Line 2'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    state = models.CharField(max_length=100, verbose_name=_('State'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal Code'))
    country = models.CharField(max_length=100, verbose_name=_('Country'))
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'))

    class Meta:
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            models.Index(fields=['postal_code']),
            models.Index(fields=['country']),
        ]
        verbose_name = _('Shipping Address')
        verbose_name_plural = _('Shipping Addresses')

    def __str__(self):
        return f"Shipping Address for Order #{self.postal_code} - {self.full_name}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_('Order ID'))
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name=_('User'))
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='orders', verbose_name=_('Shipping Address'))
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Shipping Charge'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Discount'), default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Total Amount'))
    tracking_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Tracking ID'))
    tracking_link = models.URLField(blank=True, null=True, verbose_name=_('Tracking Link'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name=_('Product Variant'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    
    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product_variant']),
        ]
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.name} (Order #{self.order.id})"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name=_('Order'))
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES, verbose_name=_('Status'))
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Changed At'))

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['changed_at']),
        ]
        verbose_name = _('Order Status History')
        verbose_name_plural = _('Order Status Histories')

    def __str__(self):
        return f"Order #{self.order.id} changed to {self.status} on {self.changed_at}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', _('Online')),
        ('cash_on_delivery', _('Cash on Delivery')),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name=_('Order'))
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name=_('Method'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    status = models.CharField(max_length=20, choices=[('pending', _('Pending')), ('completed', _('Completed')), ('failed', _('Failed'))], default='pending', verbose_name=_('Status'))
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Transaction ID'))
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Payment Date'))

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_date']),
        ]
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.method} - {self.status}"



class Refund(models.Model):
    REFUND_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('processed', _('Processed')),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds', verbose_name=_('Order'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    reason = models.TextField(verbose_name=_('Reason'))
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Transaction ID'))
    refund_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Refund Date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['refund_date']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        verbose_name = _('Refund')
        verbose_name_plural = _('Refunds')

    def __str__(self):
        return f"Refund for Order #{self.order.id} - {self.status}"
