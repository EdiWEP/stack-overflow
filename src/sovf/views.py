from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionForm
from .models import Question, Answer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class QuestionListView(ListView):
    model = Question
    template_name = "question_list.html"
    context_object_name = "questions"


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    context_object_name = "question"


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "question_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.pk})

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'question_form.html'

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            raise PermissionError("You are not authorized to edit this question.")
        return super().form_valid(form)

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'question_confirm_delete.html'
    success_url = reverse_lazy('question_list')


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    template_name = "answer_form.html"
    fields = ["content"]

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.question = question
        return super().form_valid(form)

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    template_name = "answer_form.html"
    fields = ["content"]

    def get_object(self, queryset=None):
        answer = super().get_object(queryset)
        if answer.author != self.request.user:
            raise PermissionError("You are not authorized to edit this answer.")
        return answer

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})

class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    template_name = "answer_confirm_delete.html"
    context_object_name = "answer"
    success_url = reverse_lazy("question_list")

    def get_object(self, queryset=None):
        answer = super().get_object(queryset)
        if answer.author != self.request.user:
            raise PermissionError("You are not authorized to delete this answer.")
        return answer

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy('question_detail', kwargs={'pk': question_id})