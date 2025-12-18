from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def smart_date(value):
    """
    Smart date formatter that shows:
    - "Today, HH:MM AM/PM" for today's dates
    - "DD MMM, HH:MM AM/PM" for other dates
    """
    if not value:
        return ""
    
    # Ensure timezone-aware
    if timezone.is_naive(value):
        value = timezone.make_aware(value)
    
    now = timezone.now()
    
    # Check if today
    if value.date() == now.date():
        return f"Today, {value.strftime('%I:%M %p')}"
    else:
        return value.strftime('%d %b, %I:%M %p')
