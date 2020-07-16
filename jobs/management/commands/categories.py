import os
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from jobs import models as jobs

descriptions = '''
Consectetur adipisicing elit sed do eiusmod tempor incididunt ut labore et dolore 
magna aliquaenim ad minim veniamac quis nostrud exercitation ullamco laboris...
'''


class Command(BaseCommand):
    def add_arguments(self, parser):
        return super(Command, self).add_arguments(parser)

    def handle(self, *args, **kwargs):
        seen = set()
        with open('filenames/category.txt', 'r') as freelancer_names:
            for name_row in freelancer_names:
                if name_row not in seen:
                    title = name_row
                    description = descriptions
                    slug = slugify(title)
                    category = jobs.JobsCategories.objects.create(
                        description=description,
                        name=title,
                        slug=slug,
                    )
                    category.save()
                    seen.add(name_row)

        self.stdout.write(self.style.SUCCESS('Users Generated Successfully...'))
