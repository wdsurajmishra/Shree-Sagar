from django import template
from inventory.models import ProductVariant

register = template.Library()

@register.filter
def info(id):
    variant = ProductVariant.objects.get(id=id)
    return variant