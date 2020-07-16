from django.conf import settings
from django.utils import timezone
from django.db import models

from accounts.models import AccountType, CountryModel, GenderModel, SkillModel, DepartmentModel
from jobs.models import JobsCategories, JobsListings
from utilities.managers import FreelancerManager

User = settings.AUTH_USER_MODEL


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    joined_date = models.DateField(default=timezone.now)
    gender = models.ForeignKey(GenderModel, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(CountryModel, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=150, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='freelancer_image', blank=True, default='freelancer.jpg')
    hire_rate = models.DecimalField(max_digits=5, null=True, blank=True, decimal_places=2)
    description = models.TextField()
    confirmed = models.BooleanField(default=False)
    interests = models.ManyToManyField(JobsCategories, related_name='interests', blank=True)
    account_type = models.ForeignKey(AccountType, blank=True, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    banner = models.ImageField(upload_to='freelancer_banners', default='freelancer_banner.jpg', null=True, blank=True)
    objects = FreelancerManager()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class FeedBackModel(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_company')
    date_posted = models.DateTimeField(default=timezone.now)
    feedback = models.TextField()
    behaviour = models.BooleanField(default=False)
    quality = models.BooleanField(default=False)
    deadline = models.BooleanField(default=False)
    services = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.company.company_profile.name} - {self.freelancer.freelancer_profile.get_full_name}'


class FreelancerProjects(models.Model):
    image = models.ImageField(upload_to='freelancer_project', null=True, blank=True, default='freelancer.png')
    name = models.CharField(max_length=150)
    url = models.URLField()
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_projects')

    def __str__(self):
        return self.name


class FreelancerExperience(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_experience')
    company = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class FreelancerEducation(models.Model):
    title = models.CharField(max_length=150)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_education')
    institution = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class FreelancerSkills(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    all_skills = models.ForeignKey(SkillModel, null=True, blank=True, on_delete=models.SET_NULL)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_skills')
    rate = models.IntegerField()

    def __str__(self):
        return f"{self.title}"


class FreelancerAwards(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='freelancer_awards', null=True, blank=True)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_awards')
    award_date = models.DateField(blank=True, null=True)
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'
