from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Word
import datetime


class AdminInterfaceTests(TestCase):
    def test_create_single_word_and_definition(self):
        # Define the URL for creating a word and definition
        create_word_url = reverse('flashcards:create_word')

        # Define the word and definition data to be submitted via the form
        word_data = {
            'word': 'test_word',
            'definition': 'test_definition',
        }

        # Submit the data via POST request
        response = self.client.post(create_word_url, data=word_data)

        # Check if the word was created in the database
        word = Word.objects.filter(word=word_data['word'], definition=word_data['definition']).first()
        self.assertIsNotNone(word)

        # Check if the user was redirected to the index page after creating the word
        self.assertRedirects(response, reverse('flashcards:index'))

    def setUp(self):
        # Create some sample word data for testing
        Word.objects.create(word="sample_word_1", definition="sample_definition_1")
        Word.objects.create(word="sample_word_2", definition="sample_definition_2")
        Word.objects.create(word="sample_word_3", definition="sample_definition_3")

    def test_view_cards(self):
        # Define the URL for viewing cards
        view_cards_url = reverse('flashcards:view_cards')

        # Access the view cards URL via a GET request
        response = self.client.get(view_cards_url)

        # Check if the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the correct word data
        self.assertContains(response, "sample_word_1")
        self.assertContains(response, "sample_definition_1")
        self.assertContains(response, "sample_word_2")
        self.assertContains(response, "sample_definition_2")
        self.assertContains(response, "sample_word_3")
        self.assertContains(response, "sample_definition_3")

        # Check if the response uses the correct template
        self.assertTemplateUsed(response, 'flashcards/view_cards.html')


class FlashcardLogicTests(TestCase):
    def setUp(self):
        # Create some sample word data for testing
        self.word = Word.objects.create(word="test", definition="test definition")

    def test_initial_bin(self):
        self.assertEqual(self.word.bin, 0)

    def test_moving_between_bins(self):
        # Simulate getting the word right and moving up bins
        self.word.bin = 1
        self.word.save()
        self.assertEqual(self.word.bin, 1)

        # Simulate getting the word wrong and moving back to bin 1
        self.word.bin = 5
        self.word.save()
        self.word.bin = 1
        self.word.save()
        self.assertEqual(self.word.bin, 1)

    def test_reviewing_words(self):
        # Set next_review to a past time
        past_time = timezone.now() - datetime.timedelta(minutes=5)
        self.word.next_review = past_time
        self.word.save()

        words_to_review = Word.objects.filter(next_review__lte=timezone.now()).order_by('-bin')
        self.assertEqual(words_to_review.first(), self.word)

    def test_forgetting_words(self):
        # Simulate getting the word wrong 10 times
        self.word.incorrect_count = 10
        self.word.bin = -1
        self.word.save()

        # Check if the word is in the "hard to remember" bin
        self.assertEqual(self.word.bin, -1)

    def test_review_order(self):
        # Create two additional words
        word2 = Word.objects.create(word="test2", definition="test definition 2", bin=3, next_review=timezone.now())
        word3 = Word.objects.create(word="test3", definition="test definition 3", bin=5, next_review=timezone.now())

        # Access the index URL via a GET request
        response = self.client.get(reverse('flashcards:index'))

        # Check if the word with the higher bin is shown first
        self.assertContains(response, 'test3')

        # Mark word3 as "I got it" and set the next_review for word3 to the future
        word3.bin = 6
        word3.next_review = timezone.now() + datetime.timedelta(minutes=10)
        word3.save()

        # Access the index URL via a GET request again
        response = self.client.get(reverse('flashcards:index'))

        # Check if the word with the next highest bin is shown
        self.assertContains(response, 'test2')


class UserInteractionTests(TestCase):
    def setUp(self):
        self.word = Word.objects.create(word="test", definition="test definition")

    def test_display_word(self):
        response = self.client.get(reverse('flashcards:index'))
        self.assertContains(response, 'test')

    def test_got_it_or_not(self):
        # Create a second word
        word2 = Word.objects.create(word='test2', definition='test_definition2', bin=0)

        # Test if clicking "I did not get it" processes the response correctly for the first word
        response_not_got_it = self.client.post(reverse('flashcards:index'), {'got_it': 'false'})
        self.word.refresh_from_db()
        self.assertEqual(self.word.bin, 1)  # The word should move from bin 0 to bin 1
        self.assertEqual(self.word.incorrect_count, 1)  # The incorrect_count should increment by 1

        # Test if clicking "I got it" processes the response correctly for the second word
        response_got_it = self.client.post(reverse('flashcards:index'), {'got_it': 'true'})
        word2.refresh_from_db()
        self.assertEqual(word2.bin, 1)  # The word should move from bin 0 to bin 1

    def test_status_messages(self):
        # Temporarily done message
        # Move the word to bin 11 so that there are no words left to review
        self.word.bin = 11
        self.word.next_review = None
        self.word.save()

        response = self.client.get(reverse('flashcards:index'))
        self.assertContains(response, "You are temporarily done; please come back later to review more words.")
