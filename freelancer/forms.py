from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Max, Min

from accounts import models as accounts
from freelancer import models
from jobs.models import JobsCategories

User = get_user_model()


class FreelancerFilterForm(forms.Form):
    max_hire_rate = models.FreelancerProfile.objects.aggregate(Max('hire_rate'))
    min_hire_rate = models.FreelancerProfile.objects.aggregate(Min('hire_rate'))
    freelancer_by_hourly_rate = forms.ChoiceField(
        choices=[(f'{v - 1}-{v + 9}', f'${v - 1} - ${v + 9}') for v in range(
            int(min_hire_rate['hire_rate__min']), int(max_hire_rate['hire_rate__max']),
            10)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        })
    )
    freelancer_by_profession = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Search Profession'
        }
    ), required=False)
    freelancer_by_department = forms.ModelMultipleChoiceField(
        widget=forms.RadioSelect(),
        required=False,
        queryset=accounts.DepartmentModel.objects.all()
    )
    freelancer_by_account_type = forms.ModelMultipleChoiceField(
        widget=forms.RadioSelect(),
        required=False,
        queryset=accounts.AccountType.objects.all()
    )
    search_freelancer_by_interests = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Search By Interests'
        }
    ), required=False)
    select_freelancer_by_interests = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        queryset=JobsCategories.objects.all()
    )
    freelancer_by_country = forms.ModelMultipleChoiceField(
        widget=forms.RadioSelect(),
        required=False,
        queryset=accounts.CountryModel.objects.all()
    )


class FreelancerProfileForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select Skills',
            'data-placeholder': 'Select Interests to follow',
            'style': 'display: none;'
        }), required=False,
        queryset=JobsCategories.objects.all(),
    )
    gender = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=False, empty_label='Select Gender',
        queryset=accounts.GenderModel.objects.all(),
    )
    account_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Account Type',
        queryset=accounts.AccountType.objects.all(),
    )
    country = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Country',
        queryset=accounts.CountryModel.objects.all(),
    )

    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Your Address', 'name': 'address', 'type': 'text'}
    ), required=False)

    profession = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Profession'
    }), required=False)

    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your First Name'
    }), required=False)

    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Last Name'
    }), required=False)

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Say a little bit about you '
    }), required=False)

    hire_rate = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Hire Rate ($)'
    }), required=False)

    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'filep',
        'name': 'logo',
        'type': 'file'
    }), label='Your Profile Image', required=False)

    banner = forms.ImageField(widget=forms.FileInput(attrs={
        'id': 'filew',
        'name': 'banner',
        'type': 'file'
    }), label='Your Profile Banner', required=False)

    class Meta:
        model = models.FreelancerProfile
        fields = ['account_type', 'interests', 'country', 'address', 'hire_rate',
                  'description', 'avatar', 'profession', 'first_name', 'last_name', 'banner'
                  ]


class FreelancerProjectsForm(forms.ModelForm):
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Project\'s URL (if any)'
    }))
    name = forms.CharField(label='Project\'s Name', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Project\'s Name',
    }))
    image = forms.ImageField(label='Project\'s Image', required=True, widget=forms.FileInput(attrs={
        'id': 'filen',
        'name': 'image'
    }))

    class Meta:
        model = models.FreelancerProjects
        fields = ['name', 'image', 'url']


class FreelancerAwardForm(forms.ModelForm):
    award_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Award\'s Date yyyy-mm-dd'
    }))
    title = forms.CharField(label='Award\'s Title', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Award\'s Title',
    }))
    image = forms.ImageField(label='Award\'s Image', required=True, widget=forms.FileInput(attrs={
        'id': 'file',
        'name': 'image'
    }))

    class Meta:
        model = models.FreelancerAwards
        fields = ['title', 'image', 'award_date']


class FreelancerSkillsForm(forms.ModelForm):
    all_skills = forms.ModelChoiceField(
        widget=forms.Select(attrs={
            'class': 'chosen-select Skills',
            'style': 'display: none;'
        }), required=True, empty_label='Select Skills you would like to follow',
        queryset=accounts.SkillModel.objects.all(),
    )
    rate = forms.IntegerField(label='Skills\'s Rate', max_value=100, required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rate Your Skill (0% to 100%)',
    }))
    title = forms.CharField(label='Award\'s Name', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Skills\'s Title',
    }))

    class Meta:
        model = models.FreelancerSkills
        fields = ['title', 'rate', 'all_skills']


class FreelancerExperienceForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Experiance Title',
    }))
    company = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company\'s Name',
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Brief introduction'
    }), required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Start Date yyyy-mm-dd'
    }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'End Date yyyy-mm-dd *'
    }), required=False)

    class Meta:
        model = models.FreelancerExperience
        fields = ['title', 'company', 'description', 'start_date', 'end_date']


class FreelancerEducationForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Education Title',
    }))
    institution = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'institution\'s Name',
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Brief introduction'
    }), required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Start Date yyyy-mm-dd'
    }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'End Date yyyy-mm-dd *'
    }), required=False)

    class Meta:
        model = models.FreelancerEducation
        fields = ['title', 'institution', 'description', 'start_date', 'end_date']
