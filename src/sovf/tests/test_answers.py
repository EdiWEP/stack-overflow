from django.test import TestCase
from django.urls import reverse
from sovf.models import Question
from django.contrib.auth.models import User

class AnswerCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Question Title', content='Question Content', author=self.user)
        self.url = reverse('answer_create', kwargs={'pk': self.question.pk})

    def test_unauthorized_users_cannot_post_answers(self):
        response = self.client.post(self.url, {'content': 'Test Answer'})
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(self.question.answers.exists())  

