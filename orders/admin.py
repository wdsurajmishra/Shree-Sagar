from django.contrib import admin
from django.http import HttpRequest
from .models import Order, OrderItem, OrderStatusHistory, Payment, ShippingAddress, Refund
from import_export.admin import ExportActionMixin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('product_variant', 'quantity', 'price')

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'changed_at')

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('method', 'amount', 'status', 'transaction_id', 'payment_date')

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ('full_name', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone_number')

class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_id', 'user__username', 'status')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('order_id', 'user', 'status', 'total_amount', 'shipping_address', 'shipping_charge', 'discount',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    inlines = [OrderItemInline, OrderStatusHistoryInline, PaymentInline]

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price')
    search_fields = ('order__order_id', 'product_variant__name')
    list_filter = ('order',)
    ordering = ('-order__created_at',)

# admin.site.register(OrderItem, OrderItemAdmin)

class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_at')
    search_fields = ('order__order_id', 'status')
    list_filter = ('status', 'changed_at')
    ordering = ('-changed_at',)


    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


    def has_change_permission(self, request: HttpRequest) -> bool:
        return False

# admin.site.register(OrderStatusHistory, OrderStatusHistoryAdmin)

class PaymentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('order', 'method', 'amount', 'status', 'transaction_id', 'payment_date')
    search_fields = ('order__order_id', 'method', 'status', 'transaction_id')
    list_filter = ('method', 'status', 'payment_date')
    ordering = ('-payment_date',)

admin.site.register(Payment, PaymentAdmin)

class ShippingAddressAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('customer', 'full_name', 'address_line_1', 'city', 'state', 'postal_code', 'country', 'phone_number')
    search_fields = ('order__order_id', 'full_name', 'city', 'state', 'postal_code', 'country')
    list_filter = ('city', 'state', 'country')


admin.site.register(ShippingAddress, ShippingAddressAdmin)


@admin.register(Refund)
class RefundAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('order', 'amount', 'reason', 'status', 'refund_date', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order__order_id', 'reason', 'status')
    readonly_fields = ('refund_date', 'created_at', 'updated_at')
    ordering = ('-created_at',)