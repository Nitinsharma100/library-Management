from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using a key.
    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def get_category_count(category_counts, category):
    """
    Template filter to get the count of books in a specific category.
    Usage: {{ category_counts|get_category_count:category }}
    """
    if category_counts is None or category not in category_counts:
        return 0
    return category_counts[category]['count']

@register.filter
def get_category_name(category_counts, category):
    """
    Template filter to get the display name of a category.
    Usage: {{ category_counts|get_category_name:category }}
    """
    if category_counts is None or category not in category_counts:
        return category
    return category_counts[category]['name']