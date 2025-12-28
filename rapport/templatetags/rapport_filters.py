from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplie deux valeurs"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def to_fc(value, taux):
    """Convertit USD en FC"""
    try:
        return float(value) * float(taux)
    except (ValueError, TypeError):
        return 0