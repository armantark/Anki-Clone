# Import necessary modules
import datetime

from django.db import models
from django.utils import timezone


# Define the Word model
class Word(models.Model):
    # Fields for the Word model
    word = models.CharField(max_length=100)
    definition = models.TextField()
    bin = models.IntegerField(default=0)
    next_review = models.DateTimeField(null=True, blank=True)
    incorrect_count = models.PositiveIntegerField(default=0)

    # Update bin and next_review based on whether the word was gotten or not
    def update_bin_and_next_review(self, got_it):
        # Update bin and save the model
        if got_it:
            self.bin = min(self.bin + 1, 11)
        else:
            self.incorrect_count += 1
            if self.incorrect_count >= 10:
                self.bin = -1
            else:
                self.bin = 1

        # Save the model and set the next_review
        self.save()
        self.set_next_review()

    # Set the next_review based on the current bin value
    from django.utils import timezone

    def set_next_review(self):
        # Define time_deltas for review intervals
        time_deltas = [datetime.timedelta(seconds=5), datetime.timedelta(seconds=25), datetime.timedelta(minutes=2),
                       datetime.timedelta(minutes=10), datetime.timedelta(hours=1), datetime.timedelta(hours=5),
                       datetime.timedelta(days=1), datetime.timedelta(days=5), datetime.timedelta(days=25),
                       datetime.timedelta(days=120), None]

        # Calculate the next_review_delta based on the current bin value
        next_review_delta = time_deltas[self.bin - 1] if self.bin > 0 else None
        # Set the next_review and save the model
        if next_review_delta:
            self.next_review = timezone.now() + next_review_delta
        else:
            self.next_review = None

        # Save the model
        self.save()

    # Get words to review based on their bin value and next_review date
    @classmethod
    def get_words_to_review(cls):
        # Filter words to review and order them by bin and next_review
        words_to_review = cls.objects.filter(next_review__lte=timezone.now()).order_by('-bin', 'next_review')
        # If no words to review, filter words with bin=0
        if not words_to_review.exists():
            words_to_review = cls.objects.filter(bin=0)
        # Return the words to review
        return words_to_review

    # Get a message based on the number of words to review
    @staticmethod
    def get_message():
        # Count the total number of words and completed words
        all_words_count = Word.objects.count()
        completed_words_count = Word.objects.filter(bin__in=[11, -1]).count()
        # Count the number of words to review
        words_to_review_count = Word.get_words_to_review().count()

        # Return a message based on the number of words to review
        if words_to_review_count == 0:
            if completed_words_count == all_words_count:
                return "You have no more words to review; you are permanently done!"
            else:
                return "You are temporarily done; please come back later to review more words."
        else:
            return None

    # Return the string representation of the Word model
    def __str__(self):
        return self.word
