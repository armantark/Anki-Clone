# Import necessary modules and functions
from django.conf import settings
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

    # Handle user input (got it/didn't get it) using POST request
    if request.method == 'POST':
        got_it = request.POST.get('got_it') == 'true'
        word.update_bin_and_next_review(got_it)

        # Redirect to the index view with updated words
        return redirect(reverse('flashcards:index'))

    return render(request, 'flashcards/index.html', {'word': word})


def manage_words(request, word_id=None):
    word_id = request.POST.get('word_id')
    word = get_object_or_404(Word, id=word_id) if word_id else Word()
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = WordForm(instance=word or Word())

    words = Word.objects.all()
    return render(request, 'flashcards/manage_words.html', {'form': form, 'words': words, 'word': word})



@require_POST
def delete_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    word.delete()
    return redirect('flashcards:manage_words')


def check_word(request):
    word = request.GET.get('word', '')
    exists = Word.objects.filter(word__iexact=word).exists()
    return JsonResponse({'exists': exists})


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
