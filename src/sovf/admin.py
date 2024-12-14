from django.contrib import admin
from .models import Question, Answer, Vote, AnswerVote

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'question', 'created_at')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'value', 'created_at')

@admin.register(AnswerVote)
class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'value', 'created_at')