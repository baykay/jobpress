from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import JobPressUsers


class JobPressUserCreationForm(UserCreationForm):
    class Meta:
        model = JobPressUsers
        fields = ('username', 'email', 'first_name', 'last_name', 'is_freelancer', 'is_company')


class JobPressUserUpdateForm(UserChangeForm):

    class Meta:
        model = JobPressUsers
        fields = ('username', 'email', 'first_name', 'last_name', 'is_freelancer', 'is_company')
