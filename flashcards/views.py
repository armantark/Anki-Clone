from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Word
from .forms import WordForm
import datetime
from django.conf import settings
from django.utils import timezone


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
        word_id = request.POST.get('word_id')
        if word_id:
            if got_it:
                # Move the word to the next bin, up to bin 11
                word.bin = min(word.bin + 1, 11)
            else:
                word.incorrect_count += 1

                # Check if the word has reached 10 incorrect counts
                if word.incorrect_count >= 10:
                    word.bin = -1
                else:
                    word.bin = 1

                word.save()
                word.set_next_review()

        # Update the next_review time based on the word's bin
        time_deltas = [datetime.timedelta(seconds=5), datetime.timedelta(seconds=25), datetime.timedelta(minutes=2),
                       datetime.timedelta(minutes=10), datetime.timedelta(hours=1), datetime.timedelta(hours=5),
                       datetime.timedelta(days=1), datetime.timedelta(days=5), datetime.timedelta(days=25),
                       datetime.timedelta(days=120), None]
        next_review_delta = time_deltas[word.bin - 1] if word.bin > 0 else None
        if next_review_delta:
            word.next_review = datetime.datetime.now() + next_review_delta
        else:
            word.next_review = None

        # Check if the word should be moved to the "hard to remember" bin
        if word.incorrect_count >= 10:
            word.bin = -1  # Use -1 to represent the "hard to remember" bin
            word.next_review = None

        word.save()

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
    bin_time_mapping = {
        1: "5 seconds",
        2: "25 seconds",
        3: "2 minutes",
        4: "10 minutes",
        5: "1 hour",
        6: "5 hours",
        7: "1 day",
        8: "5 days",
        9: "25 days",
        10: "120 days",
        11: "No more reviews",
        -1: "Hard to remember",
        0: "Not yet reviewed",
    }
    return render(request, 'flashcards/view_cards.html', {'cards': cards, 'bin_time_mapping': bin_time_mapping, 'DEBUG': settings.DEBUG})


