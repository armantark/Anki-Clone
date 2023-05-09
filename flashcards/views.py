from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Word
from .forms import WordForm
import datetime
from django.conf import settings
from django.utils import timezone

from .utils import bin_time_mapping


def index(request):
    # Get words that need to be reviewed, prioritizing higher-numbered bins
    words_to_review = Word.objects.filter(next_review__lte=datetime.datetime.now()).order_by('-bin', 'next_review')

    # Get a word from bin 0 if there are no words to review
    if not words_to_review.exists():
        words_to_review = Word.objects.filter(bin=0)

    # Show a message if there are no words to review and no words in bin 0
    if not words_to_review.exists():
        message = "You are temporarily done; please come back later to review more words."
        all_words = Word.objects.all()
        if all_words.filter(bin__in=[11, -1]).count() == all_words.count():
            message = "You have no more words to review; you are permanently done!"
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


def create_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flashcards:index')
    else:
        form = WordForm()
    return render(request, 'flashcards/create_word.html', {'form': form})


def view_cards(request):
    if settings.DEBUG and request.method == 'POST' and request.POST.get('make_ready'):
        cards = Word.objects.exclude(bin__in=[-1, 11])  # Exclude words in bins -1 and 11
        for card in cards:
            card.next_review = timezone.now()
            card.save()

    cards = Word.objects.all()
    return render(request, 'flashcards/view_cards.html',
                  {'cards': cards, 'bin_time_mapping': bin_time_mapping, 'DEBUG': settings.DEBUG})


