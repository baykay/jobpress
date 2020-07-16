from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import AccountType, CountryModel, DepartmentModel
from utilities.managers import CompanyProfileManager

User = settings.AUTH_USER_MODEL


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    joined_date = models.DateField(default=timezone.now)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, default='Company Name')
    tagline = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='companies', default='company.png', null=True, blank=True)
    banner = models.ImageField(upload_to='company_banners', default='company.png', null=True, blank=True)
    country = models.ForeignKey(CountryModel, null=True, blank=True, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=200, null=True, blank=True)
    employees = models.CharField(choices=[(f'{v - 1}-{v + 9}', f'{v - 1} - {v + 9}') for v in range(1, 101, 10)],
                                 max_length=10, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, blank=True, related_name='is_following')
    objects = CompanyProfileManager()

    def __str__(self):
        return self.name
