from django.shortcuts import get_object_or_404, redirect, render
from .forms import QuestionForm, RegistrationForm, ProfileForm
from .models import Question, Answer, Vote, AnswerVote, Profile
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy


class UserRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_success')

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.kwargs['username']:
            raise PermissionDenied("You are not authorized to edit another user's password")

        return super().dispatch(request, *args, **kwargs)


def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', {'message': str(exception)})

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_success.html'

class QuestionListView(ListView):
    model = Question
    template_name = "question_list.html"
    context_object_name = "questions"
    paginate_by = 10

    def get_queryset(self):
        return Question.objects.all().order_by('-created_at')

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
        return reverse_lazy("question_detail", kwargs={"pk": self.object.pk})

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "question_form.html"

    def get_success_url(self):
        return reverse_lazy("question_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        if form.instance.author != self.request.user:
            raise PermissionDenied("You are not authorized to edit this question.")
        return super().form_valid(form)

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "question_confirm_delete.html"
    success_url = reverse_lazy("question_list")


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
        return reverse_lazy("question_detail", kwargs={"pk": question_id})


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    template_name = "answer_form.html"
    fields = ["content"]

    def get_object(self, queryset=None):
        answer = super().get_object(queryset)
        if answer.author != self.request.user:
            raise PermissionDenied("You are not authorized to edit this answer.")
        return answer

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy("question_detail", kwargs={"pk": question_id})

class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    template_name = "answer_confirm_delete.html"
    context_object_name = "answer"
    success_url = reverse_lazy("question_list")

    def get_object(self, queryset=None):
        answer = super().get_object(queryset)
        if answer.author != self.request.user:
            raise PermissionDenied("You are not authorized to delete this answer.")
        return answer

    def get_success_url(self):
        question_id = self.object.question.id
        return reverse_lazy("question_detail", kwargs={"pk": question_id})

class VoteOnQuestionView(LoginRequiredMixin, View):
    def post(self, request, pk, vote_type):
        question = get_object_or_404(Question, pk=pk)

        vote_value = 1 if vote_type == 'up' else -1

        existing_vote = Vote.objects.filter(user=request.user, question=question).first()
        if existing_vote:
            existing_vote.value = vote_value
            existing_vote.save()
        else:
            Vote.objects.create(user=request.user, question=question, value=vote_value)

        return redirect('question_detail', pk=question.pk)


class VoteOnAnswerView(LoginRequiredMixin, View):
    def post(self, request, pk, vote_type):
        answer = get_object_or_404(Answer, pk=pk)

        vote_value = 1 if vote_type == 'up' else -1

        existing_vote = AnswerVote.objects.filter(user=request.user, answer=answer).first()
        if existing_vote:
            existing_vote.value = vote_value
            existing_vote.save()
        else:
            AnswerVote.objects.create(user=request.user, answer=answer, value=vote_value)

        return redirect('question_detail', pk=answer.question.pk)


class AcceptAnswerView(LoginRequiredMixin, View):
    def post(self, request, question_pk, answer_pk):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, pk=answer_pk)

        if question.author != request.user:
            raise PermissionDenied("You are not authorized to accept an answer for this question.")

        question.accepted_answer = answer
        question.save()

        return redirect('question_detail', pk=question.pk)


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile_view.html'
    context_object_name = 'profile'


    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        if username:
            user = get_object_or_404(get_user_model(), username=username)
            return user.profile

        return self.request.user.profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')
        if username != self.request.user.username:
            raise PermissionDenied("You are not authorized to edit this profile.")

        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('my_profile_view')


class SearchQuestionListView(ListView):
    model = Question
    template_name = 'search_results.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            questions = Question.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(answers__content__icontains=query)
            ).distinct().order_by('-created_at')
            return questions
        else:
            return Question.objects.all().order_by('-created_at')