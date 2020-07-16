from django import forms
from django.db.models import Q

from .models import JobsListings, Proposals, JobOffers
from accounts import models as accounts
from jobs import models as jobs


class JobOffersForm(forms.ModelForm):
    job = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job To Offer',
        queryset=JobsListings.objects.none(),
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'wt-tinymceeditor',
        'class': 'wt-tinymceeditor form-control',
        'placeholder': 'Specify Offer Details Here'
    }))

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job'].queryset = JobsListings.objects.filter(company=company).exclude(
            Q(completed=True) |
            Q(pending=False) |
            Q(proposed=True) |
            Q(hired=True)
        )

    class Meta:
        model = JobOffers
        fields = ['job', 'description']


class JobsFilterForm(forms.Form):
    search_by_category = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search By Category'
        }), required=False)
    select_by_category = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=False, empty_label='Select Job\'s Category',
        queryset=jobs.JobsCategories.objects.all(),
    )
    select_by_country = forms.ModelMultipleChoiceField(
        widget=forms.RadioSelect(),
        required=False,
        queryset=accounts.CountryModel.objects.all()
    )
    search_by_country = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search By Country'
        }), required=False)
    select_by_duration = forms.ModelMultipleChoiceField(
        widget=forms.RadioSelect(),
        required=False,
        queryset=accounts.DurationModel.objects.all()
    )
    select_by_job_type = forms.ModelMultipleChoiceField(
        widget=forms.RadioSelect(),
        required=False,
        queryset=accounts.JobTypeModel.objects.all()
    )
    select_by_skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        queryset=accounts.SkillModel.objects.all(),
    )
    select_by_department = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        queryset=accounts.DepartmentModel.objects.all(),
    )
    search_by_department = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search By Departments'
        }), required=False)


class JobsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Job Title'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'wt-tinymceeditor',
        'class': 'wt-tinymceeditor form-control',
        'placeholder': 'Add Job Detail Here'
    }))
    hire_rate = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Hire Rate ($)'
    }), required=True)
    skills = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select Skills',
            'data-placeholder': 'Skills',
            'style': 'display: none;'
        }), required=True,
        queryset=accounts.SkillModel.objects.all(),
    )
    country = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Location',
        queryset=accounts.CountryModel.objects.all(),
    )
    job_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Type',
        queryset=accounts.JobTypeModel.objects.all(),
    )
    department = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Department',
        queryset=accounts.DepartmentModel.objects.all(),
    )
    account_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Account Type',
        queryset=accounts.AccountType.objects.all(),
    )
    duration = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Duration',
        queryset=accounts.DurationModel.objects.all(),
    )
    membership = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Membership',
        queryset=accounts.MembershipModel.objects.all(),
    )
    category = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Job\'s Category',
        queryset=jobs.JobsCategories.objects.all(),
    )
    proposals_due_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Proposal Due Date (yyyy-mm-dd)'
    }), required=False)

    class Meta:
        model = JobsListings
        fields = [
            'title', 'description', 'department', 'job_type', 'country', 'account_type',
            'skills', 'category', 'duration', 'membership', 'hire_rate',
            'proposals_due_date'
        ]


class JobsProposalsForm(forms.ModelForm):
    duration = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='I Can Finish This Job In...',
        queryset=accounts.DurationModel.objects.all(),
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'wt-tinymceeditor',
        'class': 'wt-tinymceeditor form-control',
        'placeholder': 'Some More Information...'
    }), required=False)
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Charge Rate ($)',
        'type': 'number'
    }), required=True)
    attachments = forms.FileField(widget=forms.FileInput, required=False)

    class Meta:
        model = Proposals
        fields = ['duration', 'amount', 'description', 'attachments']
        # fields = ['job']
