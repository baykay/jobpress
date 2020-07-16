from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from utilities.slug_generator import slug_generator

User = get_user_model()


class HelpAndSupportType(models.Model):
    query_type = models.CharField(max_length=100)

    def __str__(self):
        return self.query_type


class HelpAndSupportModel(models.Model):
    query_type = models.ForeignKey(HelpAndSupportType, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    query = models.CharField(max_length=100)
    answer = models.TextField(null=True)

    def __str__(self):
        return self.query


class AccountSettingsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_settings')
    public_profile = models.BooleanField(default=True)
    searchable = models.BooleanField(default=True)
    show_feedback = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=User)
def create_accounts_settings(instance, created, sender, **kwargs):
    if created:
        AccountSettingsModel.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_account_settings(instance, sender, **kwargs):
    instance.account_settings.save()


class DeletedAccountsModel(models.Model):
    user_email = models.EmailField()
    reason = models.CharField(max_length=100, null=False, blank=False)
    unsubscribe = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.user_email} {self.reason}'


class EmailNotificationModel(models.Model):
    user = models.OneToOneField(User, related_name='email_notification', on_delete=models.CASCADE)
    alerts = models.BooleanField(default=True)
    updates = models.BooleanField(default=True)
    security_updates = models.BooleanField(default=True)
    data_transfer = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=User)
def notification_create(instance, created, sender, **kwargs):
    if created:
        EmailNotificationModel.objects.create(user=instance)


@receiver(post_save, sender=User)
def notification_save(instance, sender, **kwargs):
    instance.email_notification.save()


class AccountType(models.Model):
    title = models.CharField(max_length=15)
    slug = models.SlugField()
    description = models.TextField(max_length=150)
    image = models.ImageField(upload_to='accounts_image', default='freelancer.png')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jobs:jobs_accounts_list', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Account Types'


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.title, instance.slug)


pre_save.connect(slug_save, sender=AccountType)


class CountryModel(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    flag = models.ImageField(upload_to='counties_flag', default='flags.png')
    description = models.TextField(max_length=150)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jobs:jobs_countries_list', kwargs={'slug': self.slug})


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.name, instance.slug)


pre_save.connect(slug_save, sender=CountryModel)


class GenderModel(models.Model):
    name = models.CharField(max_length=7)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Genders'

    def __str__(self):
        return self.name


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.name, instance.slug)


pre_save.connect(slug_save, sender=GenderModel)


class DepartmentModel(models.Model):
    department = models.CharField(max_length=60)
    slug = models.SlugField()
    image = models.ImageField(upload_to='departments_images', default='flags.png')
    description = models.TextField(max_length=150)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department

    def get_absolute_url(self):
        return reverse('jobs:jobs_department_list', kwargs={'slug': self.slug})


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.department, instance.slug)


pre_save.connect(slug_save, sender=DepartmentModel)


class SkillModel(models.Model):
    all_skills = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(max_length=150)
    image = models.ImageField(upload_to='skills_image', default='freelancer.png')

    class Meta:
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.all_skills

    def get_absolute_url(self):
        return reverse('jobs:jobs_skills_list', kwargs={'slug': self.slug})


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.all_skills, instance.slug)


pre_save.connect(slug_save, sender=SkillModel)


class JobTypeModel(models.Model):
    type = models.CharField(max_length=20)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Job Types'

    def __str__(self):
        return self.type


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.type, instance.slug)


pre_save.connect(slug_save, sender=JobTypeModel)


class AttachmentModel(models.Model):
    attachments = models.FileField()
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Attachments'

    def __str__(self):
        return self.attachments.name


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.attachments, instance.slug)


pre_save.connect(slug_save, sender=AttachmentModel)


class MembershipModel(models.Model):
    membership = models.CharField(max_length=30)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Allowed Memberships'

    def __str__(self):
        return self.membership


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.membership, instance.slug)


pre_save.connect(slug_save, sender=MembershipModel)


class DurationModel(models.Model):
    duration = models.CharField(max_length=30)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Job Duration'

    def __str__(self):
        return self.duration


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance, instance.duration, instance.slug)


pre_save.connect(slug_save, sender=DurationModel)
