# Import necessary modules and functions
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

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
    word.is_duplicated = Word.objects.filter(word=word.word).count() > 1

    # Handle user input (got it/didn't get it) using POST request
    if request.method == 'POST':
        got_it = request.POST.get('got_it') == 'true'
        word.update_bin_and_next_review(got_it)

        # Redirect to the index view with updated words
        return redirect(reverse('flashcards:index'))

    return render(request, 'flashcards/index.html', {'word': word})


# This view function handles the creation and updating of words in the flashcard application.
def manage_words(request, word_id=None):
    # If a word_id is provided in the POST request, get that word; otherwise, create a new one.
    word_id = request.POST.get('word_id')
    word = get_object_or_404(Word, id=word_id) if word_id else Word()

    # Handle the POST request when the form is submitted.
    if request.method == 'POST':
        # Initialize the form with the POST data and the instance of the word to be updated.
        form = WordForm(request.POST, instance=word)

        # Validate the form.
        if form.is_valid():
            # Check if the word is a duplicate.
            if Word.objects.filter(word=form.cleaned_data.get('word')).exists():
                # If it is, add a warning message.
                messages.warning(request, 'Warning - word already exists, adding anyway')

            # Save the form, either creating a new word or updating an existing one.
            form.save()

            # Redirect to the same page to display the updated list of words and clear the form.
            return HttpResponseRedirect(request.path_info)

    # Handle the GET request when the page is loaded.
    else:
        # Initialize the form with the instance of the word to be updated, or a new word.
        form = WordForm(instance=word or Word())

    # Get all the words sorted by id.
    words = Word.objects.all().order_by('id')

    # Check if there is a duplicate warning for the form.
    duplicate_warning = getattr(form, 'duplicate_warning', None)

    # Render the page with the form, the list of words, the word to be updated, and any warning.
    return render(request, 'flashcards/manage_words.html',
                  {'form': form, 'words': words, 'word': word, 'duplicate_warning': duplicate_warning})


# This view function handles the deletion of words in the flashcard application.
@require_POST  # This decorator ensures that only POST requests can call this function.
def delete_word(request, word_id):
    # Retrieve the word object with the provided word_id. If it doesn't exist, return a 404 error.
    word = get_object_or_404(Word, id=word_id)

    # Delete the word object from the database.
    word.delete()

    # Redirect to the 'manage_words' page to display the updated list of words.
    return redirect('flashcards:manage_words')


# This view function handles AJAX requests to check if a word already exists in the database.
def check_word(request):
    # Get the word from the request's GET parameters. If it's not provided, default to an empty string.
    word = request.GET.get('word', '')

    # Check if a word object with a case-insensitive match to the provided word exists in the database.
    exists = Word.objects.filter(word__iexact=word).exists()

    # Return a JsonResponse with a key 'exists' indicating whether or not the word exists.
    return JsonResponse({'exists': exists})


def view_cards(request):
    # Make all cards ready for review in DEBUG mode
    if settings.DEBUG and request.method == 'POST' and request.POST.get('make_ready'):
        cards = Word.objects.exclude(bin__in=[-1, 11])  # Exclude words in bins -1 and 11
        cards = cards.filter(next_review__gt=timezone.now())
        for card in cards:
            card.next_review = timezone.now()
            card.save()
    # Get all cards and render them in the view
    cards = Word.objects.all().order_by('id')
    return render(request, 'flashcards/view_cards.html',
                  {'cards': cards, 'bin_time_mapping': bin_time_mapping, 'DEBUG': settings.DEBUG})


# self-explanatory
def about(request):
    return render(request, 'flashcards/about.html')
