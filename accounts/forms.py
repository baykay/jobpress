from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from accounts import models

User = get_user_model()


class AskHelpAndSupportForm(forms.ModelForm):
    query_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select the query type',
        queryset=models.HelpAndSupportType.objects.all(),
    )
    query = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Help And Support Description'
    }))

    class Meta:
        model = models.HelpAndSupportModel
        fields = ['query', 'query_type']


class AccountSettingsForm(forms.ModelForm):
    public_profile = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'public_profile'
    }), required=False, label='Make my profile public')
    searchable = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'searchable'
    }), required=False, label='Make my profile searchable')
    show_feedback = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'show_feedback'
    }), required=False, label='Make my clients feedback public')

    class Meta:
        model = models.AccountSettingsModel
        fields = ['searchable', 'show_feedback', 'public_profile']


class DeletedAccountsForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))
    reason = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Reason'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Description (Optional)'
    }), required=False)
    unsubscribe = forms.BooleanField(label='Unsubscribe me from all email lists',
                                     widget=forms.CheckboxInput(),
                                     required=False)


class EmailNotificationForm(forms.ModelForm):
    alerts = forms.BooleanField(label='Send me Weekly newsletter alerts', widget=forms.CheckboxInput(attrs={
        'id': 'alerts',
    }), required=False)
    updates = forms.BooleanField(label='Send me Weekly updates', widget=forms.CheckboxInput(attrs={
        'id': 'updates',
    }), required=False)
    data_transfer = forms.BooleanField(label='Send me Weekly security alerts', widget=forms.CheckboxInput(attrs={
        'id': 'data_transfer',
    }), required=False)
    security_updates = forms.BooleanField(label='Send me data transfer information', widget=forms.CheckboxInput(attrs={
        'id': 'security_updates',
    }), required=False)

    class Meta:
        model = models.EmailNotificationModel
        fields = ['alerts', 'updates', 'data_transfer', 'security_updates']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Current Password',
        }
    ))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
        }
    ))

    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }
    ))


class AccountDetailsForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))

    class Meta:
        model = User
        fields = ['email', 'username']


class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'account@email.com',
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Unique Identifier',
        }
    ), help_text='Your unique identifier is what freelancers will use to connect with you (e.g '
                 '<strong>company-name</strong> or <strong>company_name</strong>)')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'username']


class FreelancerRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'account@email.com',
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        }
    ))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UsersLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'account@email.com',
            'name': 'email'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'name': 'password',
        }
    ))
