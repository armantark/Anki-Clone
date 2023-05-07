from django.forms import ModelForm
from .models import Word


class WordForm(ModelForm):
    class Meta:
        model = Word
        fields = ['word', 'definition']
