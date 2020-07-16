from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from freelancer.forms import FreelancerFilterForm
from jobs import models as jobs
from accounts import models as accounts
from jobs.forms import JobsFilterForm
from utilities.decorators import freelancer_required_view, company_required_view


class CompanyRequired:
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(company_required_view)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)


class FreelancerRequired:
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(freelancer_required_view)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)


class ContextData:
    title = 'Add title to this view/template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_categories'] = jobs.JobsCategories.objects.all()[:8]
        context['freelancer_filter_form'] = FreelancerFilterForm(self.request.GET)
        context['footer_categories'] = jobs.JobsCategories.objects.all()[:8]
        context['footer_countries'] = accounts.CountryModel.objects.all()[:8]
        context['footer_skills'] = accounts.SkillModel.objects.all()[:8]
        context['footer_account_type'] = accounts.AccountType.objects.all()[:8]
        context['footer_departments'] = accounts.DepartmentModel.objects.all()[:8]
        context['title'] = self.get_title()
        context['title'] = self.title
        context['searchtype'] = self.request.GET.get('searchtype')
        context['search_query'] = self.request.GET.get('title')
        return context

    def get_title(self):
        return self.title


class FilterContext:
    def get_context_data(self, **kwargs):
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        context = super().get_context_data(**kwargs)
        context['form'] = JobsFilterForm(self.request.GET)
        context['search_by_category'] = search_by_category
        context['select_by_category'] = select_by_category
        context['select_by_country'] = select_by_country
        context['search_by_country'] = search_by_country
        context['select_by_department'] = select_by_department
        context['search_by_department'] = search_by_department
        context['select_by_job_type'] = select_by_job_type
        context['select_by_skills'] = select_by_skills
        context['select_by_duration'] = select_by_duration
        return context
