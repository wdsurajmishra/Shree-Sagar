from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify_admin(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "admin_notifications",
        {
            "type": "send_notification",
            "message": message,
        }
    )

def place_order(request):
    # Process the order here...
    
    # Notify the admin
    notify_admin("A new order has been placed!")

    return JsonResponse({"status": "Order placed successfully"})    


