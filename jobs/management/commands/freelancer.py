import datetime
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts import models as accounts
from jobs import models as jobs
from freelancer import models as freelancer_model
import random

User = get_user_model()
passwords = 'sysadmin'

dm = ['com', 'org', 'in', 'mail', 'info', 'co', 'io', 'ng']

ms = ['gmail', 'yahoo', 'outlook', 'aol', 'yandex']

description = '''Excepteur sint occaecat cupidatat non proident, saeunt in culpa qui officia deserunt mollit anim 
laborum. Seden utem perspiciatis undesieu omnis voluptatem accusantium doque laudantium, totam rem aiam eaqueiu ipsa 
quae ab illoion inventore veritatisetm quasitea architecto beataea dictaed quia couuntur magni dolores eos aquist 
ratione vtatem seque nesnt. Neque porro quamest quioremas ipsum quiatem dolor sitem ameteism conctetur adipisci velit 
sedate quianon. Laborum sed ut perspiciatis unde omnis iste natus error sitems voluptatem accusantium doloremque 
laudantium, totam rem aiam eaque ipsa quae ab illo inventore veritatis etna quasi architecto beatae vitae dictation 
explicabo. nemo enim ipsam fugit. '''


def generate_date_added():
    year = random.randint(2020, 2020)
    month = random.randint(1, 11)
    day = random.randint(1, 26)
    return datetime.date(year, month, day)


def generate_account_type():
    obj = random.randint(1, 7)
    types = accounts.AccountType.objects.get(id=obj)
    return types


def generate_gender():
    obj = random.randint(1, 2)
    types = accounts.GenderModel.objects.get(id=obj)
    return types


def generate_country():
    obj = random.randint(1, 190)
    types = accounts.CountryModel.objects.get(id=obj)
    return types


def generate_department():
    obj = random.randint(0, 42)
    try:
        types = accounts.DepartmentModel.objects.get(id=obj)
    except accounts.DepartmentModel.DoesNotExist:
        return accounts.DepartmentModel.objects.first()
    return types


def freelancer_interests_gen():
    obj = random.randint(1, 40)
    try:
        types = jobs.JobsCategories.objects.get(id=obj)
    except jobs.JobsCategories.DoesNotExist:
        return jobs.JobsCategories.objects.first()
    return types


hire_rate = f'{random.randint(10, 99)}.{random.randint(20, 90)}'


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super(Command, self).add_arguments(parser)

    def handle(self, *args, **kwargs):
        with open('filenames/freelancer_name.txt', 'r') as freelancer_detail:
            for row in freelancer_detail:
                name_email_profession_address = row.split('-')
                freelancer_name = name_email_profession_address[0]

                freelancer_username = slugify(name_email_profession_address[0]).replace(' ', '').lower()
                email = f'{freelancer_username}@{random.choice(ms)}.{random.choice(dm)}'
                first_name = freelancer_name.split(' ')[0]
                last_name = freelancer_name.strip().split(' ')[1]

                country = generate_country()
                profession = name_email_profession_address[1]
                address = name_email_profession_address[2]
                department = generate_department()
                account_type = generate_account_type()
                date_added = generate_date_added()
                freelancer_description = description
                freelancer_interests = freelancer_interests_gen()

                freelancer_user = User.objects.create_user(
                    email=email, is_freelancer=True, username=freelancer_username,
                    )
                freelancer_user.set_password(passwords)
                freelancer_user.save()

                company_to_save = freelancer_model.FreelancerProfile.objects.create(
                    user=freelancer_user, gender=generate_gender(), account_type=account_type, country=country,
                    joined_date=date_added, address=address, confirmed=True, department=department,
                    description=freelancer_description, profession=profession, hire_rate=float(hire_rate),
                    first_name=first_name, last_name=last_name
                )
                company_to_save.save()
                company_to_save.interests.add(freelancer_interests)
                print(freelancer_username, passwords)

        self.stdout.write(self.style.SUCCESS('Users Generated Successfully...'))
