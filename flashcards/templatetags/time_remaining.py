from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def time_remaining(value):
    if not value:
        return ''

    now = timezone.now()
    time_difference = value - now

    if time_difference.total_seconds() <= 0:
        prefix = 'Ready ('
        suffix = ' ago)'
    else:
        prefix = ''
        suffix = ''

    seconds = int(abs(time_difference.total_seconds()))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

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

    time_str += suffix

    return time_str

