# Import the template module from Django
from django import template

# Create a new instance of the template Library
register = template.Library()


# Register a custom template filter using the decorator syntax
@register.filter
def get_item(dictionary, key):
    # Return the value associated with the given key in the dictionary, or None if the key is not present
    return dictionary.get(key)
