from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from jobs import models as jobs
from accounts import models as accounts
import datetime
import random

User = get_user_model()

hire_rates = random.randint(11.00, 99.00)


def generate_date_added():
    year = random.randint(2020, 2020)
    month = random.randint(1, 11)
    day = random.randint(1, 26)
    return datetime.date(year, month, day)


def generate_account_type():
    obj = random.randint(1, 8)
    types = accounts.AccountType.objects.get(id=obj)
    return types


def generate_memberships():
    obj = random.randint(1, 5)
    try:
        types = accounts.MembershipModel.objects.get(id=obj)
    except accounts.MembershipModel.DoesNotExist:
        return accounts.MembershipModel.objects.first()
    return types


def generate_job_types():
    obj = random.randint(1, 5)
    try:
        types = accounts.JobTypeModel.objects.get(id=obj)
    except accounts.JobTypeModel.DoesNotExist:
        return accounts.JobTypeModel.objects.first()
    return types


def generate_countrys():
    obj = random.randint(1, 191)
    try:
        types = accounts.CountryModel.objects.get(id=obj)
    except accounts.CountryModel.DoesNotExist:
        return accounts.CountryModel.objects.first()
    return types


def generate_department():
    obj = random.randint(0, 42)
    try:
        types = accounts.DepartmentModel.objects.get(id=obj)
    except accounts.DepartmentModel.DoesNotExist:
        return accounts.DepartmentModel.objects.first()
    return types


def generate_company():
    obj = random.randint(700, 1400)
    try:
        types = User.objects.get(is_company=True, id=obj)
    except User.DoesNotExist:
        return User.objects.first()
    return types


def generate_category():
    obj = random.randint(1, 81)
    try:
        types = jobs.JobsCategories.objects.get(id=obj)
    except jobs.JobsCategories.DoesNotExist:
        return jobs.JobsCategories.objects.first()
    return types


def generate_duration():
    obj = random.randint(1, 4)
    try:
        types = accounts.DurationModel.objects.get(id=obj)
    except accounts.DurationModel.DoesNotExist:
        return accounts.DurationModel.objects.first()
    return types


def generate_skills():
    obj = random.randint(1, 127)
    try:
        types = accounts.SkillModel.objects.get(id=str(obj))
    except accounts.SkillModel.DoesNotExist:
        return accounts.SkillModel.objects.first()
    return types


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super(Command, self).add_arguments(parser)

    def handle(self, *args, **kwargs):
        with open('filenames/jobs_listings.txt', 'r') as titles:
            for row in titles:
                account_type = generate_account_type()
                category = generate_category()
                title = row
                hire_rate = hire_rates
                membership = generate_memberships()
                country = generate_countrys()
                job_type = generate_job_types()
                duration = generate_duration()
                description = '''Nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit inati
                              voluptate velit esse cillum dolore eutates fugiat nulla pariatur sunt in culpa asequi 
                              officia deserunt mollit anim id est laborum ut perspiciatis...'''
                skills = generate_skills()
                proposals_due_date = generate_date_added()
                companies = generate_company()
                department = generate_department()

                jobslistings = jobs.JobsListings(account_type=account_type, category=category, title=title,
                                                 hire_rate=hire_rate, membership=membership, country=country,
                                                 job_type=job_type, duration=duration, description=description,
                                                 proposals_due_date=proposals_due_date, slug=slugify(title),
                                                 company=companies, department=department)
                jobslistings.save()
                jobslistings.skills.add(skills)

        self.stdout.write(self.style.SUCCESS('Jobs Generated Successfully...'))
