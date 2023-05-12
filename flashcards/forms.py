# Import the ModelForm class from Django's forms module
from django import forms
from django.forms import ModelForm

# Import the Word model from the current app's models module
from .models import Word


# Define a custom form class called WordForm that inherits from ModelForm
class WordForm(ModelForm):
    duplicate_warning = forms.CharField(max_length=255, required=False, widget=forms.HiddenInput())

    # Specify the Meta class within WordForm to provide model and fields information

    class Meta:
        # Set the model for this form to be the Word model
        model = Word
        # Specify the fields to be included in the form
        fields = ['word', 'definition', 'duplicate_warning']

    # This method is part of Django's form validation process.
    # It specifically validates and cleans the 'word' field.
    def clean_word(self):
        # Get the 'word' field from the cleaned_data dictionary.
        word = self.cleaned_data.get('word')

        # Check if a Word object with the same 'word' already exists in the database.
        if Word.objects.filter(word=word).exists():
            # If a duplicate is found, set a warning message.
            self.duplicate_warning = 'Warning - word already exists, adding anyway'

        # Return the cleaned 'word' data.
        return word
