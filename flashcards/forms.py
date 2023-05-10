# Import the ModelForm class from Django's forms module
from django.forms import ModelForm

# Import the Word model from the current app's models module
from .models import Word


# Define a custom form class called WordForm that inherits from ModelForm
class WordForm(ModelForm):
    # Specify the Meta class within WordForm to provide model and fields information
    class Meta:
        # Set the model for this form to be the Word model
        model = Word
        # Specify the fields to be included in the form
        fields = ['word', 'definition']
