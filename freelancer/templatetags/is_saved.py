from django import template
from django.shortcuts import get_object_or_404

from freelancer.models import FreelancerProfile
from jobs.models import JobsListings

register = template.Library()


@register.simple_tag(name='is_saved')
def is_saved(job_slug, freelancer):
    request_job = get_object_or_404(JobsListings, slug=job_slug)
    if request_job in freelancer.saved_jobs.all():
        return True
    else:
        return False
