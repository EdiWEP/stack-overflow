from django.db import models
from django.conf import settings


UPVOTE = 1
DOWNVOTE = -1

VOTE_CHOICES = [
    (UPVOTE, 'up'),
    (DOWNVOTE, 'down'),
]


class Question(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")

    def score(self) -> int:
        """Returns the question's score: upvotes - downvotes"""
        upvotes = self.votes.filter(value=UPVOTE).count()
        downvotes = self.votes.filter(value=DOWNVOTE).count()
        return upvotes - downvotes


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def score(self):
        """Returns the answers's score: upvotes - downvotes"""
        upvotes = self.votes.filter(value=UPVOTE).count()
        downvotes = self.votes.filter(value=DOWNVOTE).count()
        return upvotes - downvotes

class AnswerVote(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answer_votes',
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')