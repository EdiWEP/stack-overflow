from django import forms
from .models import Question, Profile
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.conf import settings

class RegistrationForm(UserCreationForm):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ['username', 'email', 'password1', 'password2']

class QuestionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Question
        fields = ['title', 'content']

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']