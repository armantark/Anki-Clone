# Import the AppConfig class from the Django apps module
from django.apps import AppConfig


# Define a custom configuration class for the Flashcards app, which inherits from AppConfig
class FlashcardsConfig(AppConfig):
    # Set the default auto-generated field type for primary keys in the app's models
    default_auto_field = 'django.db.models.BigAutoField'

    # Specify the name of the app, which is used by Django to identify it
    name = 'flashcards'
