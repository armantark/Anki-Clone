# Create your models here.
from django.db import models
import datetime


class Word(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()
    bin = models.IntegerField(default=0)
    next_review = models.DateTimeField(null=True, blank=True)
    incorrect_count = models.PositiveIntegerField(default=0)

    def update_bin_and_next_review(self, got_it):
        if got_it:
            self.bin = min(self.bin + 1, 11)
        else:
            self.incorrect_count += 1
            if self.incorrect_count >= 10:
                self.bin = -1
            else:
                self.bin = 1

        self.save()
        self.set_next_review()

    def set_next_review(self):
        time_deltas = [datetime.timedelta(seconds=5), datetime.timedelta(seconds=25), datetime.timedelta(minutes=2),
                       datetime.timedelta(minutes=10), datetime.timedelta(hours=1), datetime.timedelta(hours=5),
                       datetime.timedelta(days=1), datetime.timedelta(days=5), datetime.timedelta(days=25),
                       datetime.timedelta(days=120), None]

        next_review_delta = time_deltas[self.bin - 1] if self.bin > 0 else None
        if next_review_delta:
            self.next_review = datetime.datetime.now() + next_review_delta
        else:
            self.next_review = None

        self.save()

    @classmethod
    def get_words_to_review(cls):
        words_to_review = cls.objects.filter(next_review__lte=datetime.datetime.now()).order_by('-bin', 'next_review')
        if not words_to_review.exists():
            words_to_review = cls.objects.filter(bin=0)
        return words_to_review

    def __str__(self):
        return self.word
