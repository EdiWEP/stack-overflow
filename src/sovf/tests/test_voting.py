from django.test import TestCase
from django.urls import reverse
from sovf.models import Question
from django.contrib.auth import get_user_model


class VoteOnQuestionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.question = Question.objects.create(title='Question Title', content='Question Content', author=self.user)
        self.url = reverse('vote_on_question', kwargs={'pk': self.question.pk, 'vote_type': 'up'})

    def test_unauthorized_users_cannot_vote(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(self.question.votes.count(), 0)  


class QuestionUpvoteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.question = Question.objects.create(title='Question Title', content='Question Content', author=self.user)
        self.url = reverse('vote_on_question', kwargs={'pk': self.question.pk, 'vote_type': 'up'})

    def test_upvote_changes_question_score_by_plus_one(self):
        self.client.login(username='testuser', password='password')
        self.client.post(self.url)
        self.question.refresh_from_db()
        self.assertEqual(self.question.score(), 1) 


class QuestionDownvoteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.question = Question.objects.create(title='Question Title', content='Question Content', author=self.user)
        self.url = reverse('vote_on_question', kwargs={'pk': self.question.pk, 'vote_type': 'down'})

    def test_downvote_changes_question_score_by_minus_one(self):
        self.client.login(username='testuser', password='password')
        self.client.post(self.url)
        self.question.refresh_from_db()
        self.assertEqual(self.question.score(), -1)
