from django import template

register = template.Library()

@register.filter(name='to_ordinal')
def to_ordinal(n):
    """
    Adds English ordinal suffix
    """
    key_value = 4 if 10 <= n % 100 < 20 else n % 10
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(key_value, "th")

