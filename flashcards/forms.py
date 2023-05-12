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

    def clean_word(self):
        # Get the cleaned 'word' data from the form
        word = self.cleaned_data.get('word')

        # Check if the word already exists in the Word model
        if Word.objects.filter(word=word).exists():
            # If it does, add an error message to the form
            self.add_error('word', 'Warning - word already exists')

        # Return the cleaned word data
        return word
