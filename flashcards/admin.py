# Import the admin module from Django's contrib package
from django.contrib import admin

# Register your models here.
# Import the Word model from the models module in the current package
from .models import Word

# Register the Word model with the Django admin site
admin.site.register(Word)
