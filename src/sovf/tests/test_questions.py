from django.test import TestCase
from django.urls import reverse
from sovf.models import Question
from django.contrib.auth import get_user_model

class QuestionDetailViewTest(TestCase):
    def test_404_for_non_existent_question(self):
        response = self.client.get(reverse('question_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

class QuestionUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.question = Question.objects.create(title='Original Title', content='Original Content', author=self.user)
        self.url = reverse('question_edit', kwargs={'pk': self.question.pk})

    def test_logged_in_user_can_update_own_question(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {'title': 'Updated Title', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 302) 
        self.question.refresh_from_db()
        self.assertEqual(self.question.title, 'Updated Title')
        self.assertEqual(self.question.content, 'Updated Content')

class QuestionDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.question = Question.objects.create(title='Question Title', content='Question Content', author=self.user)
        self.url = reverse('question_delete', kwargs={'pk': self.question.pk})

    def test_logged_in_user_can_delete_own_question(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())


class UnauthorizedQuestionDeleteTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='user1', password='password')
        self.user2 = get_user_model().objects.create_user(username='user2', password='password')
        self.question = Question.objects.create(title='Question Title', content='Question Content', author=self.user1)
        self.url = reverse('question_delete', kwargs={'pk': self.question.pk})

    def test_unauthorized_users_cannot_delete_another_users_question(self):
        self.client.login(username='user2', password='password')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Question.objects.filter(pk=self.question.pk).exists())

    def test_authenticated_user_can_delete_own_question(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('question_list'))
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())

