from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.utils import timezone
from datetime import timedelta
from accounts.models import Customer
from orders.models import Order

# Create your models here.

class Agent(User):
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = ProcessedImageField(
        upload_to='profile_pictures',
        processors=[ResizeToFit(500, 500)],
        format='WEBP',
        options={'quality': 100},
        blank=True,
        null=True
    )
    is_avaliable = models.BooleanField(default=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'support_agent_user'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()

    def is_otp_valid(self, otp):
        if self.otp == otp and self.otp_created_at + timedelta(minutes=10) > timezone.now():
            return True
        return False
    

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="ticket_customer")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    assigned_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.status}"


class ChatMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    is_agent_message = models.BooleanField(default=False)  # Distinguish between user and agent messages
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} at {self.created_at}"
    
    def save(self, *args, **kwargs):
        if self.is_agent_message:
            self.sender = self.ticket.assigned_agent
        super().save(*args, **kwargs)