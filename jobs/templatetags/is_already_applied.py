from django import template
from jobs.models import Proposals

register = template.Library()


@register.simple_tag(name='is_already_applied')
def is_already_applied(job, freelancer):
    applied = Proposals.objects.filter(job=job, freelancer=freelancer).first()
    if applied:
        return True
    else:
        return False