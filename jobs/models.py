from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone

from accounts import models as accounts
from utilities.slug_generator import slug_generator

User = settings.AUTH_USER_MODEL


class JobsCategories(models.Model):
    name = models.CharField(max_length=70, null=True, blank=True)
    date_added = models.DateField(default=timezone.now, null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=150)
    image = models.ImageField(upload_to='jobs_categories', null=True, blank=True, default='category.png')
    slug = models.SlugField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jobs:jobs_categories_list', kwargs={'slug': self.slug})


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.name, instance.slug)


pre_save.connect(slug_save, sender=JobsCategories)


class JobsListings(models.Model):
    account_type = models.ForeignKey(accounts.AccountType, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(JobsCategories, on_delete=models.DO_NOTHING, related_name='jobs')
    title = models.CharField(max_length=100, null=True, blank=True)
    hire_rate = models.DecimalField(decimal_places=2, default=50.99, max_digits=5)
    membership = models.ForeignKey(accounts.MembershipModel, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(accounts.CountryModel, on_delete=models.DO_NOTHING)
    job_type = models.ForeignKey(accounts.JobTypeModel, on_delete=models.DO_NOTHING)
    duration = models.ForeignKey(accounts.DurationModel, on_delete=models.DO_NOTHING)
    description = models.TextField()
    skills = models.ManyToManyField(accounts.SkillModel)
    proposals_due_date = models.DateField()
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, max_length=255)
    date_added = models.DateTimeField(default=timezone.now)
    department = models.ForeignKey(accounts.DepartmentModel, on_delete=models.DO_NOTHING)
    saves = models.ManyToManyField(User, related_name='saved_jobs')
    hired = models.BooleanField(default=False, editable=True)
    proposed = models.BooleanField(default=False, editable=True)
    completed = models.BooleanField(default=False, editable=True)
    pending = models.BooleanField(default=True, editable=False)
    hired_freelancer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=True,
                                         blank=True, related_name='hired_freelancer')
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug': self.slug})


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.title, instance.slug)


pre_save.connect(slug_save, sender=JobsListings)


class JobViews(models.Model):
    job = models.ForeignKey(JobsListings, on_delete=models.CASCADE, related_name='job_views', null=True)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='view_freelancer', null=True)


class Proposals(models.Model):
    hired = 'hired (On Going)'
    completed = 'completed'
    job_status = [
        ('hired', hired),
        ('completed', completed),
    ]
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(JobsListings, on_delete=models.CASCADE, null=True)
    proposal_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2, default=20.00)
    duration = models.ForeignKey(accounts.DurationModel, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    attachments = models.FileField(blank=True, null=True)
    status = models.CharField(choices=job_status, default=hired, max_length=20)
    slug = models.SlugField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.freelancer)


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.freelancer, instance.slug)
        if instance.slug in ['delete', 'update', 'create']:
            instance.slug = slug_generator(instance, instance.freelancer, instance.slug)


pre_save.connect(slug_save, sender=Proposals)


class JobOffers(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company')
    job = models.ForeignKey(JobsListings, on_delete=models.CASCADE)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.freelancer} - {self.job}'


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.freelancer, instance.slug)


pre_save.connect(slug_save, sender=JobOffers)


class JobsReportedIssues(models.Model):
    logger = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    job = models.ForeignKey(JobsListings, on_delete=models.CASCADE, related_name='issue_job')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_freelancer')
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_company')
    issue = models.TextField()
    attachment = models.FileField(upload_to='issue_attachments', verbose_name='Issue Attachment', null=True, blank=True)

    def __str__(self):
        return self.issue[30]
