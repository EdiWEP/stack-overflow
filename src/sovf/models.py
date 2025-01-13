from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from .badges import check_for_badge_awards

UPVOTE = 1
DOWNVOTE = -1

VOTE_CHOICES = [
    (UPVOTE, "up"),
    (DOWNVOTE, "down"),
]


class Question(models.Model):

    title = models.CharField(max_length=200)
    content = RichTextUploadingField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    accepted_answer = models.ForeignKey("Answer", null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_for")

    def score(self) -> int:
        """Returns the question's score: upvotes - downvotes"""
        upvotes = self.votes.filter(value=UPVOTE).count()
        downvotes = self.votes.filter(value=DOWNVOTE).count()
        return upvotes - downvotes


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "question")


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    content = RichTextUploadingField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
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
        related_name="answer_votes",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "answer")

class AnswerComment(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answer_comments",
    )
    content = RichTextUploadingField()
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
        related_name="answer_comment_votes",
    )
    comment = models.ForeignKey(
        AnswerComment,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")


class Badge(models.Model):
    BADGE_TYPE_CHOICES = [
        ("upvotes_received", "Upvotes Received"),
        ("answers_accepted", "Answers Accepted"),
        ("questions_posted", "Questions Posted"),
        ("answers_posted", "Answers Posted"),
        ("comments_posted", "Comments Posted"),
    ]

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    threshold = models.IntegerField(help_text="The number required to achieve this badge")
    badge_type = models.CharField(
        max_length=50,
        choices=BADGE_TYPE_CHOICES,
        help_text="The type of milestone this badge tracks"
    )
    image = models.ImageField(
        upload_to="badges/",
        null=False,
        help_text="The image associated with this badge",
        default="badges/default_badge.png",
    )


    def check_eligibility(self, user):
        """Determine if the user is eligible for this badge based on badge_type"""
        badge_type_checkers = {
            "upvotes_received": self._check_upvotes_received,
            "answers_accepted": self._check_answers_accepted,
            "questions_posted": self._check_questions_posted,
            "answers_posted": self._check_answers_posted,
            "comments_posted": self._check_comments_posted,
        }

        badge_award_check_func = badge_type_checkers.get(self.badge_type)
        if badge_award_check_func:
            return badge_award_check_func(user)

        return False

    def _check_upvotes_received(self, user):
        """Check if the user has enough upvotes to earn this badge"""
        total_upvotes = (
            Vote.objects.filter(question__author=user, value=UPVOTE).count() +
            AnswerVote.objects.filter(answer__author=user, value=UPVOTE).count() +
            AnswerCommentVote.objects.filter(comment__author=user, value=UPVOTE).count()
        )
        return total_upvotes >= self.threshold

    def _check_answers_accepted(self, user):
        """Check if the user has enough accepted answers to earn this badge
        Don't count answers that the user accepted to their own questions"""
        return user.answers.filter(~Q(accepted_for=None) & ~Q(accepted_for__author=user)).count()

    def _check_questions_posted(self, user):
        """Check if the user has posted enough questions to earn this badge"""
        return user.questions.count() >= self.threshold

    def _check_answers_posted(self, user):
        """Check if the user has posted enough answers to earn this badge"""
        return user.answers.count() >= self.threshold

    def _check_comments_posted(self, user):
        """Check if the user has posted enough comments to earn this badge"""
        return user.answer_comments.count() >= self.threshold



class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="user_badges")
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge")


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

# Signal handler to create a profile when a new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal handler to save the profile when the user is updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# Signal handler for checking badge awards after user creates objects
@receiver(post_save, sender=Question)
@receiver(post_save, sender=Answer)
@receiver(post_save, sender=AnswerComment)
def check_badges_after_object_creation(sender, instance, **kwargs):
    check_for_badge_awards(instance.author)

# Signal handler for checking badge awards after a user's objects are upvoted
@receiver(post_save, sender=Vote)
@receiver(post_save, sender=AnswerVote)
@receiver(post_save, sender=AnswerCommentVote)
def check_badges_after_vote_creation(sender, instance, **kwargs):
    if instance.value != UPVOTE:
        return

    if isinstance(instance, Vote):
        check_for_badge_awards(instance.question.author)
    if isinstance(instance, AnswerVote):
        check_for_badge_awards(instance.answer.author)
    if isinstance(instance, AnswerCommentVote):
        check_for_badge_awards(instance.comment.author)
