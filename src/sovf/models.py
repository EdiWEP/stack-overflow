from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    accepted_answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_for")

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

class AnswerComment(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answer_comments',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def score(self):
        """Returns the comment's score: upvotes - downvotes"""
        upvotes = self.votes.filter(value=UPVOTE).count()
        downvotes = self.votes.filter(value=DOWNVOTE).count()
        return upvotes - downvotes

class AnswerCommentVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answer_comment_votes',
    )
    comment = models.ForeignKey(
        AnswerComment,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

# Signal handler to create a profile when a new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal handler to save the profile when the user is updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()