from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Lesson, News, UserGroups, CodeGroups


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',)


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title_ru', 'title_kk', 'title_en', 'photo', 'content', 'countQuestion', 'basic')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title_ru', 'title_kk', 'title_en', 'content_ru', 'content_kk', 'content_en', 'img')


class UserGroupsForm(forms.ModelForm):
    class Meta:
        model = UserGroups
        fields = ('name',)


class ENTForm(forms.ModelForm):
    class Meta:
        model = CodeGroups
        fields = '__all__'
