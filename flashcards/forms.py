# Import the ModelForm class from Django's forms module
from django import forms
from django.forms import ModelForm

# Import the Word model from the current app's models module
from .models import Word


# Define a custom form class called WordForm that inherits from ModelForm
class WordForm(ModelForm):
    warning = forms.CharField(max_length=255, required=False, widget=forms.HiddenInput())
    # Specify the Meta class within WordForm to provide model and fields information

    class Meta:
        # Set the model for this form to be the Word model
        model = Word
        # Specify the fields to be included in the form
        fields = ['word', 'definition', 'warning']

    # todo: make this work again
    def clean(self):
        cleaned_data = super().clean()
        word = cleaned_data.get('word')

        if Word.objects.filter(word=word).exists():
            cleaned_data['warning'] = 'Warning - word already exists, adding anyway'

        return cleaned_data
