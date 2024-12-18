from django.contrib import admin
from .models import Question, Answer, Vote, AnswerVote, AnswerComment, AnswerCommentVote, Badge, UserBadge

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("content", "author", "question", "created_at")

@admin.register(AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
    list_display = ("content", "author", "answer", "created_at")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "value", "created_at")

@admin.register(AnswerVote)
class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = ("user", "answer", "value", "created_at")

@admin.register(AnswerCommentVote)
class AnswerCommentVoteAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "value", "created_at")

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "badge_type", "threshold", "image")

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "awarded_at")