from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class JobPressUsers(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    username = models.CharField(verbose_name=_('unique identifier'), max_length=40, unique=True,
                                help_text='this is what freelancers will use to connect with you')
    is_company = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)

    def __str__(self):
        user = ' (F)' if self.is_freelancer else ' (C)'
        return f'{self.email} -{user}'

    def get_absolute_url(self):
        if self.is_company:
            return reverse('company:company_detail', kwargs={'username': self.username})
        if self.is_freelancer:
            return reverse('freelancer:detail', kwargs={'username': self.username})
