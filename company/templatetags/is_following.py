from django import template
from company.models import CompanyProfile

register = template.Library()


@register.simple_tag(name='is_following')
def is_following(company, freelancer):
    followed_company = CompanyProfile.objects.get(user=company)
    if freelancer in followed_company.followers.all():
        return True
    else:
        return False

