from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory
from notifications.views import notify_admin

@receiver(pre_save, sender=Order)
def create_order_status_history(sender, instance, **kwargs):
    # Check if the order already exists (i.e., not a new instance)
    if instance.pk:
        # Fetch the previous version of the order from the database
        previous_order = Order.objects.get(pk=instance.pk)
        # Check if the status has changed
        if previous_order.status != instance.status:
            # Create a new OrderStatusHistory record
            OrderStatusHistory.objects.create(
                order=instance,
                status=instance.status,
            )

@receiver(post_save, sender=Order)
def update_order_status_history(sender, instance, created, **kwargs):
    # If a new order is created, log its initial status
    if created:
        notify_admin(f"New order created Order {instance.id} has been created.")
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status,
        )
