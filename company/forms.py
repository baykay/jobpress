from django import forms

from accounts.models import AccountType, CountryModel
from company.models import CompanyProfile
from jobs.models import Proposals, JobsReportedIssues
from freelancer.models import FeedBackModel


class FeedbackForm(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Please provide a suitable feedback.'
    }))
    behaviour = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'behaviour'
    }), label='Was i professional?', required=False)
    quality = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'quality'
    }), label='Did i provide a quality job?', required=False)
    deadline = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'deadline'
    }), label='Was I focused to deadline?', required=False)
    services = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'services'
    }), label='Was my services worth it?', required=False)

    class Meta:
        model = FeedBackModel
        fields = ['feedback', 'behaviour', 'quality', 'deadline', 'services']


class JobsReportedIssuesForm(forms.ModelForm):
    attachment = forms.FileField(widget=forms.FileInput(), required=True)
    issue = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe Status...'
    }))

    class Meta:
        model = JobsReportedIssues
        fields = ['issue', 'attachment']


class HiredJobProposalStatus(forms.ModelForm):
    class Meta:
        model = Proposals
        fields = ['status']


class CompanyUpdateForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        empty_label='Select your account type',
        queryset=AccountType.objects.all(),
        widget=forms.Select(),
        required=True,
    )
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Company\'s name',

    }), required=False)
    tagline = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your company\'s tagline here'
    }), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your company\'s description'
    }))

    logo = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'filep',
        'name': 'logo',
        'type': 'file'
    }), label='Company\'s Logo', required=False)

    banner = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'filew',
        'name': 'banner',
        'type': 'file'
    }), label='Company\'s Banner', required=False)

    country = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Your Country',
        queryset=CountryModel.objects.all(),
    )

    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Address',
        'name': 'address',
        'type': 'text'
    }), required=False)

    # employees = forms.CharField(widget=forms.Select())

    class Meta:
        model = CompanyProfile()
        exclude = ('user', 'confirmed', 'joined_date',)
