from django.test import TestCase
from django.urls import reverse
from sovf.models import Question

class UserRegistrationTest(TestCase):
    def test_invalid_registration_form(self):
        response = self.client.post(reverse('register'), {
            'username': '', 
            'password1': 'password',
            'password2': 'different_password',  
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'This field is required.') 
        self.assertContains(response, 'The two password fields didn’t match.')  