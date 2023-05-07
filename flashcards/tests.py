from django.test import TestCase
from django.urls import reverse
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

    def test_view_cards(self):
        pass  # Write test logic here


class FlashcardLogicTests(TestCase):
    def test_initial_bin(self):
        word = Word.objects.create(word="test", definition="test definition")
        self.assertEqual(word.bin, 0)

    def test_moving_between_bins(self):
        pass  # Write test logic here

    def test_reviewing_words(self):
        pass  # Write test logic here

    def test_forgetting_words(self):
        pass  # Write test logic here


class UserInteractionTests(TestCase):
    def test_display_word(self):
        pass  # Write test logic here

    def test_show_definition(self):
        pass  # Write test logic here

    def test_got_it_or_not(self):
        pass  # Write test logic here

    def test_status_messages(self):
        pass  # Write test logic here
