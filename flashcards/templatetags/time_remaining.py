# Import necessary libraries from Django
from django import template
from django.utils import timezone

# Create a template library instance
register = template.Library()


# Register a custom filter for the template library
@register.filter
# This is used to show the time remaining or how long a word has been ready in the view_cards table
def time_remaining(value):
    # Return empty string if the input value is None or empty
    if not value:
        return ''

    # Get the current time
    now = timezone.now()
    # Calculate the time difference between the input value and current time
    time_difference = value - now

    # Check if the time difference is negative (past) or positive (future)
    if time_difference.total_seconds() <= 0:
        prefix = 'Ready ('
        suffix = ' ago)'
    else:
        prefix = ''
        suffix = ''

    # Calculate the absolute time difference in seconds, minutes, hours, and days
    seconds = int(abs(time_difference.total_seconds()))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    # Build the time remaining string based on the calculated values
    time_str = prefix
    if days:
        time_str += f'{days}d '
    if hours:
        time_str += f'{hours}h '
    if minutes:
        time_str += f'{minutes}m '

    # Remove the space before the seconds when the word is ready for review
    if time_difference.total_seconds() <= 0:
        time_str += f'{seconds}s'
    else:
        time_str += f' {seconds}s'

    # Add the suffix to the time remaining string
    time_str += suffix

    # Return the final time remaining string
    return time_str
