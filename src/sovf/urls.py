from django.urls import path
from .views import (
    QuestionListView,
    QuestionDetailView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,
    AnswerCreateView,
    AnswerUpdateView,
    AnswerDeleteView,
)

urlpatterns = [
    path('', QuestionListView.as_view(), name='question_list'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/new/', QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/edit/', QuestionUpdateView.as_view(), name='question_edit'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    path('question/<int:pk>/answer/new/', AnswerCreateView.as_view(), name='answer_create'),
    path('answer/<int:pk>/edit/', AnswerUpdateView.as_view(), name='answer_edit'),
    path('answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
]
