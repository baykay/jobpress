import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts import models as accounts
from company import models as company_model
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


def generate_country():
    obj = random.randint(1, 190)
    types = accounts.CountryModel.objects.get(id=obj)
    return types


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super(Command, self).add_arguments(parser)

    def handle(self, *args, **kwargs):
        with open('filenames/company_name.txt', 'r') as company_detail:
            for row in company_detail:
                name_email_tagline_address = row.split('-')
                company_username = slugify(name_email_tagline_address[0].replace(' ', '').lower())
                email = f'{company_username}@{random.choice(ms)}.{random.choice(dm)}'
                country = generate_country()
                name = name_email_tagline_address[0]
                tagline = name_email_tagline_address[1]
                address = name_email_tagline_address[2]
                account_type = generate_account_type()
                date_added = generate_date_added()
                comp_description = description

                company_user = User.objects.create_user(email=email, is_company=True, username=company_username)
                company_user.set_password(passwords)
                company_user.save()

                company_to_save = company_model.CompanyProfile.objects.create(
                    user=company_user,  tagline=tagline, account_type=account_type, country=country, name=name,
                    joined_date=date_added, address=address, confirmed=True,
                    description=comp_description
                )
                company_to_save.save()

        self.stdout.write(self.style.SUCCESS('Users Generated Successfully...'))
