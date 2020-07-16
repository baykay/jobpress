from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404

from jobs.models import JobsListings


class CompanyProfileManager(models.Manager):
    def follow_company(self, company, freelancer):
        from company.models import CompanyProfile
        request_freelancer = freelancer
        request_company = get_object_or_404(CompanyProfile,
                                            user__is_company=True,
                                            user__username__iexact=company)
        is_following = False
        if request_freelancer in request_company.followers.all():
            request_company.followers.remove(request_freelancer)
        else:
            request_company.followers.add(request_freelancer)
            is_following = True
        return is_following


class FreelancerQuerySet(models.QuerySet):
    def freelancers_queryset(self, title):
        title = title.split()
        first_name = [_first for _first in title]
        last_name = [_last for _last in title]
        return self.filter(Q(first_name__in=first_name) |
                           Q(last_name__in=last_name))


class FreelancerManager(models.Manager):
    def get_queryset(self):
        return FreelancerQuerySet(self.model, using=self._db)

    def freelancer_queryset(self, title):
        return self.get_queryset().freelancers_queryset(title)

    def save_job(self, job_to_save, freelancer):
        from freelancer.models import FreelancerProfile
        request_freelancer = freelancer
        request_job = get_object_or_404(JobsListings,
                                        slug__iexact=job_to_save)
        is_saved = False
        if request_job in request_freelancer.saved_jobs.all():
            request_freelancer.saved_jobs.remove(request_job)
        else:
            request_freelancer.saved_jobs.add(request_job)
            is_saved = True
        return is_saved
