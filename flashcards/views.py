# Import necessary modules and functions
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import WordForm
from .models import Word
from .utils import bin_time_mapping


def index(request):
    # Get words that need to be reviewed, prioritizing higher-numbered bins
    words_to_review = Word.get_words_to_review()

    # Show a message if there are no words to review and no words in bin 0
    message = Word.get_message()
    if message:
        return render(request, 'flashcards/index.html', {'message': message})

    # Select the first word to review
    word = words_to_review.first()

    # Handle user input (got it/didn't get it) using POST request
    if request.method == 'POST':
        got_it = request.POST.get('got_it') == 'true'
        word.update_bin_and_next_review(got_it)

        # Redirect to the index view with updated words
        return redirect(reverse('flashcards:index'))

    return render(request, 'flashcards/index.html', {'word': word})


def manage_words(request, word_id=None):
    # Check if a word_id is provided
    if word_id:
        # If so, retrieve the Word instance with the given ID, or return a 404 error if not found
        word = get_object_or_404(Word, id=word_id)
    else:
        # If no word_id is provided, create a new Word instance
        word = Word()

    # Check if the request method is POST (i.e. form submission)
    if request.method == 'POST':
        # Create a WordForm instance with the submitted data and the current Word instance
        form = WordForm(request.POST, instance=word)

        # Check if the form data is valid
        if form.is_valid():
            # Save the Word instance with the submitted data
            form.save()

            # Redirect the user to the index page
            return redirect('flashcards:index')
    else:
        # If the request method is not POST, create an empty WordForm instance with the current Word
        form = WordForm(instance=word)

    # Retrieve all words for displaying
    words = Word.objects.all()

    # Render the manage_words template with the form, words, and current word instances
    return render(request, 'flashcards/manage_words.html', {'form': form, 'words': words, 'word': word})


def delete_word(request, word_id=None):
    return render(request, 'flashcards/manage_words.html', {})


def view_cards(request):
    # Make all cards ready for review in DEBUG mode
    if settings.DEBUG and request.method == 'POST' and request.POST.get('make_ready'):
        cards = Word.objects.exclude(bin__in=[-1, 11])  # Exclude words in bins -1 and 11
        for card in cards:
            card.next_review = timezone.now()
            card.save()
    # Get all cards and render them in the view
    cards = Word.objects.all()
    return render(request, 'flashcards/view_cards.html',
                  {'cards': cards, 'bin_time_mapping': bin_time_mapping, 'DEBUG': settings.DEBUG})


