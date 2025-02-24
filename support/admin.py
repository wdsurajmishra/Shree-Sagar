from django.contrib import admin
from .models import SupportTicket, ChatMessage, Agent
from django.contrib.auth.models import User


def assign_agent_to_ticket(ticket):
    available_agents = Agent.objects.filter(is_avaliable=True)
    assigned_agent = None
    for agent in available_agents:
        if agent.assigned_tickets.filter(status="IN_PROGRESS").count() < 5:  # Example limit
            assigned_agent = agent
            break

    if assigned_agent:
        ticket.assigned_agent = assigned_agent
        ticket.status = "IN_PROGRESS"
        ticket.save()
    return assigned_agent


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_id', 'status', 'assigned_agent', 'created_at']
    actions = ['assign_agents']

    def assign_agents(self, request, queryset):
        for ticket in queryset:
            assign_agent_to_ticket(ticket)
        self.message_user(request, "Agents assigned successfully.")
    assign_agents.short_description = "Assign Agents to Tickets"

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'message', 'is_agent_message', 'created_at']
