import random
from django.core.management.base import BaseCommand
from accounts import models as accounts

from django.contrib.auth import get_user_model

Users = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super(Command, self).add_arguments(parser)

    def handle(self, *args, **kwargs):
        for user in Users.objects.filter(is_freelancer=True):
            if user.email == 'youthprogram@aol.mail':
                pass
            print(user)
            try:
                user.freelancer_profile.interests.add(random.randint(5, 10))
                user.save()
            except:
                continue

        self.stdout.write(self.style.SUCCESS('Interests Generated Successfully...'))
