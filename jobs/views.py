from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from company import models as company
from freelancer import models as freelancer
from jobs import models as jobs
from accounts import models as accounts
from jobs.forms import JobsProposalsForm, JobsFilterForm, JobOffersForm
from jobs.models import JobViews
from utilities.mixins import ContextData, FilterContext, FreelancerRequired, CompanyRequired

User = get_user_model()


class JobOfferView(CompanyRequired, ContextData, CreateView):
    form_class = JobOffersForm
    template_name = 'make_offer.html'
    slug_url_kwarg = 'username'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        freelancer_ = self.get_object().freelancer_profile.get_full_name
        offering_job = get_object_or_404(jobs.JobsListings,
                                         id=self.request.POST.get('job'))
        offering_company = self.request.user
        offering_freelancer = jobs.JobOffers.objects.filter(
            freelancer=self.get_object(), job=offering_job, company=self.request.user
        )
        if offering_freelancer.exists():
            messages.info(request, f'You have already offered <em>{offering_job}</em> to {freelancer_}')
            return redirect('freelancer:detail', self.get_object().username)

        if form.is_valid():
            subject = f'<em>{offering_company}</em> Offered You a Job'
            current_site = get_current_site(request)
            email_message = render_to_string('email_job_offering_alert.html',
                                             {
                                                 'offering_job': offering_job,
                                                 'offering_company': offering_company,
                                                 'current_site': current_site.domain
                                             })
            send_email = EmailMessage(subject, email_message, to=[self.get_object().email])
            send_email.send()
            messages.success(request, f'You have successfully offered <em>{offering_job} to <em>{freelancer_}</em>')
            return self.form_valid(form)

    def form_valid(self, form):
        form.instance.company = self.request.user
        form.instance.freelancer = self.get_object()
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(JobOfferView, self).get_form_kwargs()
        kwargs['company'] = self.request.user
        return kwargs

    def get_queryset(self):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super(JobOfferView, self).get_context_data(**kwargs)
        context['freelancer_for_offer'] = self.get_queryset()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(User, username__iexact=self.kwargs['username'])

    def get_success_url(self):
        return reverse('freelancer:detail', kwargs={'username': self.kwargs['username']})


class SearchView(FilterContext, ContextData, ListView):
    template_name = 'listings/joblistings.html'
    context_object_name = 'search_queryset'
    model = jobs.JobsListings
    paginate_by = 6

    def get_queryset(self):
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        title = self.request.GET.get('title')
        searchtype = self.request.GET.get('searchtype')
        if select_by_job_type:
            select_by_job_type = accounts.JobTypeModel.objects.get(id=select_by_job_type)
            jobs_queryset = jobs.JobsListings.objects.filter(Q(job_type=select_by_job_type))
            pluralize = 's' if jobs_queryset.count() > 1 else ''
            self.title = f'{jobs_queryset.count()} Result{pluralize} found for {select_by_job_type}'
            self.context_object_name = 'joblistings'
            return jobs_queryset
        if select_by_department or search_by_department:
            if select_by_department and search_by_department:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(department__department__icontains=search_by_department) |
                    Q(department__id__in=select_by_department) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                department = f'{select_by_department} & {search_by_department}'
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {department}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
            elif select_by_department:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(department__id__in=select_by_department) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {select_by_department}'
                self.context_object_name = 'joblistings'
                return jobs_queryset

            elif search_by_department:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(department__department__icontains=search_by_department) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {search_by_department}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
        if select_by_skills:
            jobs_queryset = jobs.JobsListings.objects.filter(
                Q(skills__id__in=select_by_skills) &
                Q(completed=False) &
                Q(hired=False)
            )
            pluralize = 's' if jobs_queryset.count() > 1 else ''
            self.title = f'{jobs_queryset.count()} Result{pluralize} found for {select_by_skills}'
            self.context_object_name = 'joblistings'
            return jobs_queryset
        if select_by_duration:
            jobs_queryset = jobs.JobsListings.objects.filter(
                Q(duration__id=select_by_duration) &
                Q(completed=False) &
                Q(hired=False)
            )
            pluralize = 's' if jobs_queryset.count() > 1 else ''
            self.title = f'{jobs_queryset.count()} Result{pluralize} found for {select_by_duration}'
            self.context_object_name = 'joblistings'
            return jobs_queryset
        if select_by_country or search_by_country:
            if select_by_country and search_by_country:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(country__name__icontains=search_by_country) |
                    Q(country__id=select_by_country) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                country = f'{select_by_country} & {search_by_country}'
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {country}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
            elif search_by_country:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(country__name__icontains=search_by_country) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {search_by_country}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
            elif select_by_country:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(country__id=select_by_country) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {select_by_country}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
        if search_by_category or select_by_category:
            if search_by_category and select_by_category:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(category__name__icontains=search_by_category) |
                    Q(category__id=select_by_category) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                category = f'{search_by_category} & {select_by_category}'
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {category}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
            elif search_by_category:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(category__name__icontains=search_by_category) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {search_by_category}'
                self.context_object_name = 'joblistings'
                return jobs_queryset
            elif select_by_category:
                jobs_queryset = jobs.JobsListings.objects.filter(
                    Q(category__id=select_by_category) &
                    Q(completed=False) &
                    Q(hired=False)
                )
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {select_by_category}'
                self.context_object_name = 'joblistings'
                return jobs_queryset

        if title and searchtype:
            if searchtype == 'job':
                if title:
                    jobs_queryset = self.model.objects.filter(
                        Q(title__icontains=title) &
                        Q(completed=False) &
                        Q(hired=False)
                    )
                    pluralize = 's' if jobs_queryset.count() > 1 else ''
                    self.title = f'{jobs_queryset.count()} Result{pluralize} found for {title}'
                    self.template_name = 'listings/joblistings.html'
                    self.context_object_name = 'joblistings'
                    return jobs_queryset

            if searchtype == 'freelancer':
                if title:
                    freelancer_queryset = freelancer.FreelancerProfile.objects.freelancer_queryset(title)
                    pluralize = 's' if freelancer_queryset.count() > 1 else ''
                    self.title = f'{freelancer_queryset.count()} Result{pluralize} found for {title}'
                    self.template_name = 'freelancer_list.html'
                    self.context_object_name = 'freelancers'
                    return freelancer_queryset

            if searchtype == 'company':
                if title:
                    company_queryset = company.CompanyProfile.objects.filter(name__icontains=title)
                    pluralize = 's' if company_queryset.count() > 1 else ''
                    self.title = f'{company_queryset.count()} Result{pluralize} found for {title}'
                    self.template_name = 'companieslist.html'
                    self.context_object_name = 'companies'
                    return company_queryset
        if title and not searchtype:
            request_user = self.request.user
            if request_user.is_authenticated and request_user.is_freelancer:
                jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False) &
                    Q(title__icontains=title)
                ).distinct()
                self.context_object_name = 'joblistings'
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Job{pluralize} found for {title}'
                return jobs_queryset
            elif request_user.is_authenticated and request_user.is_company:
                jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False) &
                    Q(title__icontains=title)
                )
                self.context_object_name = 'joblistings'
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {title}'
                return jobs_queryset
            else:
                jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False)
                )
                self.context_object_name = 'joblistings'
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {title}'
                return jobs_queryset
        elif searchtype and not title:
            if searchtype == 'job':
                request_user = self.request.user
                if request_user.is_authenticated and request_user.is_freelancer:
                    jobs_by_feed = self.model.objects.filter(
                        Q(completed=False) &
                        Q(hired=False) &
                        Q(category__in=request_user.freelancer_profile.interests.all()) &
                        Q(account_type=request_user.freelancer_profile.account_type)
                    ).distinct()
                    if not jobs_by_feed:
                        jobs_by_feed = self.model.objects.filter(
                            Q(completed=False) &
                            Q(hired=False) &
                            Q(category__in=request_user.freelancer_profile.interests.all()) |
                            Q(account_type=request_user.freelancer_profile.account_type)
                        ).distinct()
                    self.context_object_name = 'joblistings'
                    pluralize = 's' if jobs_by_feed.count() > 1 else ''
                    self.title = f'{jobs_by_feed.count()} Job{pluralize} found based on your your profile'
                    return jobs_by_feed
                elif request_user.is_authenticated and request_user.is_company:
                    jobs_by_feed = self.model.objects.filter(
                        Q(completed=False) &
                        Q(hired=False) &
                        Q(country=request_user.company_profile.country) |
                        Q(account_type=request_user.company_profile.account_type)
                    ).distinct()
                    if not jobs_by_feed:
                        jobs_by_feed = self.model.objects.filter(
                            Q(completed=False) &
                            Q(hired=False) &
                            Q(country=request_user.company_profile.country) |
                            Q(account_type=request_user.company_profile.account_type)
                        ).distinct()
                    self.context_object_name = 'joblistings'
                    self.title = 'Jobs based on your country and account type'
                    pluralize = 's' if jobs_by_feed.count() > 1 else ''
                    self.title = f'{jobs_by_feed.count()} Job{pluralize} found based on your your profile'
                    return jobs_by_feed
                else:
                    jobs_by_feed = self.model.objects.filter(
                        Q(completed=False) &
                        Q(hired=False)
                    ).distinct()
                    self.context_object_name = 'joblistings'
                    self.title = 'Jobs based on your country and account type'
                    pluralize = 's' if jobs_by_feed.count() > 1 else ''
                    self.title = f'{jobs_by_feed.count()} Job{pluralize} found based on your your profile'
                    return jobs_by_feed

            elif searchtype == 'freelancer':
                request_user = self.request.user
                if request_user.is_authenticated and request_user.is_freelancer:
                    freelancer_queryset = freelancer.FreelancerProfile.objects.filter(
                        Q(interests__in=request_user.freelancer_profile.interests.all()) &
                        Q(account_type=request_user.freelancer_profile.account_type)
                    ).distinct()
                    if not freelancer_queryset:
                        freelancer_queryset = freelancer.FreelancerProfile.objects.filter(
                            Q(interests__in=request_user.freelancer_profile.interests.all()) |
                            Q(account_type=request_user.freelancer_profile.account_type)
                        ).distinct()
                    pluralize = 's' if freelancer_queryset.count() > 1 else ''
                    self.context_object_name = 'freelancers'
                    self.title = f'{freelancer_queryset.count()} Freelancer{pluralize} found based on your profile'
                    self.template_name = 'freelancer_list.html'
                    return freelancer_queryset
                elif request_user.is_authenticated and request_user.is_company:
                    freelancer_queryset = freelancer.FreelancerProfile.objects.filter(
                        Q(country=request_user.company_profile.country) &
                        Q(account_type=request_user.company_profile.account_type)
                    )
                    if not freelancer_queryset:
                        freelancer_queryset = freelancer.FreelancerProfile.objects.filter(
                            Q(country=request_user.company_profile.country) |
                            Q(account_type=request_user.company_profile.account_type)
                        )
                    pluralize = 's' if freelancer_queryset.count() > 1 else ''
                    self.context_object_name = 'freelancers'
                    self.template_name = 'freelancer_list.html'
                    self.title = f'{freelancer_queryset.count()} Freelancer{pluralize} found based on your profile'
                    return freelancer_queryset
                else:
                    freelancer_queryset = freelancer.FreelancerProfile.objects.all()
                    pluralize = 's' if freelancer_queryset.count() > 1 else ''
                    self.context_object_name = 'freelancers'
                    self.template_name = 'freelancer_list.html'
                    self.title = f'{freelancer_queryset.count()} Freelancer{pluralize} found based on your profile'
                    return freelancer_queryset
            elif searchtype == 'company':
                request_user = self.request.user
                if request_user.is_authenticated and request_user.is_freelancer:
                    company_queryset = company.CompanyProfile.objects.filter(
                        Q(country=request_user.freelancer_profile.country) &
                        Q(account_type=request_user.freelancer_profile.account_type)
                    ).distinct()
                    if not company_queryset:
                        company_queryset = company.CompanyProfile.objects.filter(
                            Q(country=request_user.freelancer_profile.country) |
                            Q(account_type=request_user.freelancer_profile.account_type)
                        ).distinct()
                    pluralize = 'Companies' if company_queryset.count() > 1 else 'Company'
                    self.context_object_name = 'companies'
                    self.template_name = 'companieslist.html'
                    self.title = f'{company_queryset.count()} {pluralize} found based on your profile'
                    return company_queryset
                elif request_user.is_authenticated and request_user.is_company:
                    company_queryset = company.CompanyProfile.objects.filter(
                        Q(country=request_user.company_profile.country) &
                        Q(account_type=request_user.company_profile.account_type)
                    ).distinct()
                    if not company_queryset:
                        company_queryset = company.CompanyProfile.objects.filter(
                            Q(country=request_user.company_profile.country) |
                            Q(account_type=request_user.company_profile.account_type)
                        ).distinct()
                    pluralize = 'Companies' if company_queryset.count() > 1 else 'Company'
                    self.context_object_name = 'companies'
                    self.template_name = 'companieslist.html'
                    self.title = f'{company_queryset.count()} {pluralize} found based on your profile'
                    return company_queryset
                else:
                    company_queryset = company.CompanyProfile.objects.all()
                    pluralize = 'Companies' if company_queryset.count() > 1 else 'Company'
                    self.context_object_name = 'companies'
                    self.template_name = 'companieslist.html'
                    self.title = f'{company_queryset.count()} {pluralize} found based on your profile'
                    return company_queryset
            else:
                return self.get_queryset()
        else:
            request_user = self.request.user
            if request_user.is_authenticated and request_user.is_freelancer:
                jobs_by_feed = self.model.objects.filter(
                    Q(category__in=request_user.freelancer_profile.interests.all()) &
                    Q(account_type=request_user.freelancer_profile.account_type)
                ).distinct()
                self.context_object_name = 'joblistings'
                self.title = 'Jobs based on your account and interests'
                return jobs_by_feed
            elif request_user.is_authenticated and request_user.is_company:
                random_jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False) &
                    Q(country=request_user.company_profile.country) |
                    Q(account_type=request_user.company_profile.account_type)
                )
                self.context_object_name = 'joblistings'
                self.title = 'Jobs based on your country and account type'
                return random_jobs_queryset
            else:
                jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False)
                )
                self.context_object_name = 'joblistings'
                pluralize = 's' if jobs_queryset.count() > 1 else ''
                self.title = f'{jobs_queryset.count()} Result{pluralize} found for {title}'
                return jobs_queryset

    def get_company(self):
        company_queryset = company.CompanyProfile.objects.filter(
            name__icontains=self.request.GET.get('title')).values('name', )
        if company_queryset is not None:
            return company_queryset
        else:
            return company.CompanyProfile.objects.all()

    def get_freelancers(self):
        title = self.request.GET.get('title')
        if title:
            return freelancer.FreelancerProfile.objects.freelancer_queryset(
                title=title)

    def get_total_jobs(self):
        total_jobs = self.model.objects.filter(
            title__icontains=self.request.GET.get('title')).values('title', )
        if total_jobs is not None:
            return total_jobs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JobsFilterForm(self.request.GET)
        context['total_company_count'] = self.get_company
        context['total_freelancer_count'] = self.get_freelancers
        context['total_job_count'] = self.get_total_jobs

        return context


class MakeProposalView(FreelancerRequired, ContextData, CreateView):
    model = jobs.Proposals
    template_name = 'make_proposal.html'
    form_class = JobsProposalsForm

    def get_queryset(self):
        return jobs.JobsListings.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(MakeProposalView, self).get_context_data(**kwargs)
        context['job_to_propose'] = self.get_queryset()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(jobs.JobsListings, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('jobs:job_detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        form.instance.freelancer = self.request.user
        form.instance.job = self.get_object()
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        proposing_freelancer = jobs.Proposals.objects.filter(
            freelancer_id=self.request.user.id, job__slug=self.kwargs['slug'])
        if proposing_freelancer:
            messages.info(self.request, 'You have already sent your proposal')
            return redirect('jobs:job_detail', slug=self.kwargs['slug'])
        form = self.get_form()
        if form.is_valid():
            proposed_job = get_object_or_404(jobs.JobsListings, slug=self.kwargs['slug'])
            proposed_job.proposed = True
            proposed_job.save()
            company_email = proposed_job.company.email
            subject = f'New Proposal Received On {proposed_job.title}'
            current_site = get_current_site(request)
            email_message = render_to_string('email_proposal_alert.html',
                                             {
                                                 'proposed_job': proposed_job,
                                                 'proposed_user': self.request.user,
                                                 'current_site': current_site.domain
                                             })
            send_email = EmailMessage(subject, email_message, to=[company_email])
            send_email.send()
            messages.success(request, 'You have applied for this job')
            return self.form_valid(form)
        else:
            messages.error(request, 'Sorry An error occurred')
            return redirect('jobs:job_detail', slug=self.kwargs['slug'])


class JobsDetailView(ContextData, DetailView):
    model = jobs.JobsListings
    template_name = 'jobdetail.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        request_user = self.request.user
        job_slug = self.kwargs.get('slug')
        job = get_object_or_404(jobs.JobsListings, slug=job_slug)
        if request_user.is_authenticated:
            job_view = JobViews.objects.filter(job=job, freelancer=request_user)
            if job_view.exists():
                job.view_count = job.view_count
            else:
                JobViews.objects.get_or_create(job=job, freelancer=request_user)
                job.view_count += 1
                job.save()
        return job


class JobsListingsView(FilterContext, ContextData, ListView):
    template_name = 'listings/joblistings.html'
    model = jobs.JobsListings
    context_object_name = 'joblistings'
    paginate_by = 6
    title = 'Jobs in JobPress'

    def get_context_data(self, **kwargs):
        context = super(JobsListingsView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self):
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        if select_by_job_type:
            select_by_job_type = accounts.JobTypeModel.objects.get(id=select_by_job_type)
            return jobs.JobsListings.objects.filter(
                Q(job_type=select_by_job_type)
            )
        if select_by_department or search_by_department:
            if select_by_department and search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(department__department__contains=search_by_department) |
                    Q(department__id__in=select_by_department)
                )
            elif select_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(department__id__in=select_by_department)
                )
            elif search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(department__department__contains=search_by_department)
                )
        if select_by_skills:
            return jobs.JobsListings.objects.filter(
                Q(skills__id__in=select_by_skills)
            )
        if select_by_duration:
            return jobs.JobsListings.objects.filter(
                Q(duration__id=select_by_duration)
            )
        if select_by_country or search_by_country:
            if select_by_country and search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(country__name__contains=search_by_country) |
                    Q(country__id=select_by_country)
                )
            elif search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(country__name__icontains=search_by_country)
                )
            elif select_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(country__id=select_by_country)
                )
        if search_by_category or select_by_category:
            if search_by_category and select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(category__name__icontains=search_by_category) |
                    Q(category__id=select_by_category)
                )
            elif search_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(category__name__icontains=search_by_category)
                )
            elif select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(category__id=select_by_category)
                )
        else:
            request_user = self.request.user
            if request_user.is_authenticated and request_user.is_freelancer:
                requesting_user = User.objects.get(id=request_user.id)
                companies_id = [x.user.id for x in requesting_user.is_following.all()]
                if not companies_id:
                    self.title = 'Jobs based on your account and interests'
                    return self.model.objects.filter(
                        Q(category__in=request_user.freelancer_profile.interests.all()) &
                        Q(account_type=request_user.freelancer_profile.account_type)
                    ).distinct().order_by('-date_added')
                else:
                    self.title = 'Jobs By Companies you followed'
                    return self.model.objects.filter(company__id__in=companies_id,
                                                     company__is_company=True,
                                                     ).distinct().order_by('-date_added')
            elif request_user.is_authenticated and request_user.is_company:
                random_jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False) &
                    Q(country=request_user.company_profile.country) |
                    Q(account_type=request_user.company_profile.account_type)
                )
                return random_jobs_queryset
            else:  # if the request user is not authenticated
                jobs_queryset = self.model.objects.filter(
                    Q(completed=False) &
                    Q(hired=False)
                )
                return jobs_queryset


class BrowseAllJobs(FilterContext, ContextData, ListView):
    template_name = 'listings/joblistings.html'
    model = jobs.JobsListings
    context_object_name = 'joblistings'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(BrowseAllJobs, self).get_context_data(**kwargs)
        context['title'] = 'All Jobs In JobPress'
        return context


class JobsByFollowedCompanies(FreelancerRequired, FilterContext, ContextData, ListView):
    template_name = 'listings/joblistings.html'
    model = jobs.JobsListings
    context_object_name = 'joblistings'
    paginate_by = 6
    title = ''

    def get_context_data(self, **kwargs):
        context = super(JobsByFollowedCompanies, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self):
        request_freelancer = self.request.user
        if request_freelancer.is_authenticated and request_freelancer.is_freelancer:
            requesting_user = User.objects.get(id=request_freelancer.id)
            companies_id = [company_id.user.id for company_id in requesting_user.is_following.all()]
            if companies_id:
                self.title = 'Jobs By Companies you followed'
                return self.model.objects.filter(
                    Q(company__id__in=companies_id) &
                    Q(company__is_company=True)).distinct().order_by('-date_added')
            else:
                self.title = 'Jobs By Similar Companies By Accounts'
                return self.model.objects.filter(
                    Q(category__in=request_freelancer.freelancer_profile.interests.all()) &
                    Q(account_type=request_freelancer.freelancer_profile.account_type)
                ).distinct().order_by('-date_added')
        else:
            jobs_by_feed = self.model.objects.all().order_by('-date_added')
        return jobs_by_feed


class DepartmentListView(ContextData, ListView):
    model = accounts.DepartmentModel
    template_name = 'filters/all-departments.html'
    context_object_name = 'departments'
    paginate_by = 6


class CountriesListView(ContextData, ListView):
    model = accounts.CountryModel
    template_name = 'filters/all-countries.html'
    context_object_name = "countries"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(CountriesListView, self).get_context_data(**kwargs)
        return context


class JobsByDepartmentsList(FilterContext, ContextData, ListView):
    model = accounts.DepartmentModel
    template_name = 'listings/joblistings.html'
    context_object_name = 'joblistings'
    paginate_by = 6

    def get_title(self):
        title = accounts.DepartmentModel.objects.get(slug=self.kwargs.get('slug'))
        return f'Jobs By {title.department} Department'

    def get_queryset(self):
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        if select_by_country or search_by_country:
            if select_by_country and search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(department__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country) &
                    Q(country__id=select_by_country)
                ).order_by('-date_added')
            elif search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(department__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country)
                ).order_by('-date_added')
            elif select_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(department__slug=self.kwargs.get('slug')) &
                    Q(country__id=select_by_country)
                ).order_by('-date_added')
        if select_by_job_type:
            select_by_job_type = accounts.JobTypeModel.objects.get(id=select_by_job_type)
            return jobs.JobsListings.objects.filter(
                Q(department__slug=self.kwargs.get('slug')) &
                Q(job_type=select_by_job_type)
            ).order_by('-date_added')
        if select_by_duration:
            select_by_duration = accounts.DurationModel.objects.get(id=select_by_duration)
            return jobs.JobsListings.objects.filter(
                Q(department__slug=self.kwargs.get('slug')) &
                Q(duration_id=select_by_duration)
            ).order_by('-date_added')
        if select_by_skills:
            return jobs.JobsListings.objects.filter(
                Q(department__slug=self.kwargs.get('slug')) &
                Q(skills__id__in=set(select_by_skills))
            ).order_by('-date_added')
        if search_by_category or select_by_category:
            if search_by_category and select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(department__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category) &
                    Q(category__id=select_by_category)
                ).order_by('-date_added')
            elif search_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(department__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category)
                ).order_by('-date_added')
            elif select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(department__slug=self.kwargs.get('slug')) &
                    Q(category__id=select_by_category)
                ).order_by('-date_added')
        else:
            department = jobs.JobsListings.objects.filter(
                department__slug=self.kwargs.get('slug')).order_by('-date_added')
            return department


class CategoriesListView(ContextData, ListView):
    model = jobs.JobsCategories
    template_name = 'filters/all-categories.html'
    context_object_name = 'categories'
    paginate_by = 6


class JobsByCategoryList(FilterContext, ContextData, ListView):
    model = jobs.JobsCategories
    template_name = 'listings/joblistings.html'
    context_object_name = 'joblistings'
    paginate_by = 6

    def get_queryset(self):
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')

        if select_by_job_type:
            select_by_job_type = accounts.JobTypeModel.objects.get(id=select_by_job_type)
            return jobs.JobsListings.objects.filter(
                Q(category__slug=self.kwargs.get('slug')) &
                Q(job_type=select_by_job_type)
            )
        if select_by_country or search_by_country:
            if select_by_country and search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(category__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country) &
                    Q(country__id=select_by_country)
                )
            elif search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(category__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country)
                )
            elif select_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(category__slug=self.kwargs.get('slug')) &
                    Q(country__id=select_by_country)
                )
        if select_by_duration:
            select_by_duration = accounts.DurationModel.objects.get(id=select_by_duration)
            return jobs.JobsListings.objects.filter(
                Q(category__slug=self.kwargs.get('slug')) &
                Q(duration_id=select_by_duration)
            )
        if select_by_skills:
            return jobs.JobsListings.objects.filter(
                Q(category__slug=self.kwargs.get('slug')) &
                Q(skills__id__in=select_by_skills)
            )
        if select_by_department or search_by_department:
            if select_by_department and search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(category__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department) &
                    Q(department__id__in=select_by_department)
                )
            elif select_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(category__slug=self.kwargs.get('slug')) &
                    Q(department__id__in=select_by_department)
                )
            elif search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(category__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department)
                )
        else:
            jobs_by_feed = jobs.JobsListings.objects.filter(category__slug=self.kwargs.get('slug'))
            return jobs_by_feed
            # when this site grows i will enable this

            # _freelancer = self.request.user
            # if _freelancer.is_authenticated and _freelancer.is_freelancer:
            #     jobs_by_feed = jobs.JobsListings.objects.filter(
            #         Q(category__slug=self.kwargs.get('slug')) &
            #         Q(country=_freelancer.freelancer_profile.country)
            #     ).distinct()
            # else:
            #     jobs_by_feed = jobs.JobsListings.objects.filter(category__slug=self.kwargs.get('slug'))
            # return jobs_by_feed

    def get_title(self):
        title = self.model.objects.get(slug__iexact=self.kwargs.get('slug'))
        return f'Jobs By {title.name} Category'


class SkillsListView(ContextData, ListView):
    model = jobs.accounts.SkillModel
    template_name = 'filters/all-skills.html'
    context_object_name = 'skills'
    paginate_by = 6


class JobsBySkillsList(FilterContext, ContextData, ListView):
    model = accounts.SkillModel
    template_name = 'listings/joblistings.html'
    context_object_name = 'joblistings'
    paginate_by = 6

    def get_queryset(self):
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        if select_by_duration:
            return jobs.JobsListings.objects.filter(
                Q(skills__slug=self.kwargs.get('slug')) &
                Q(duration__id=select_by_duration)
            )
        if select_by_job_type:
            return jobs.JobsListings.objects.filter(
                Q(skills__slug=self.kwargs.get('slug')) &
                Q(job_type__id=select_by_job_type)
            )
        if select_by_department or search_by_department:
            if select_by_department and search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department) &
                    Q(department__id__in=select_by_department)
                )
            elif select_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(department__id__in=select_by_department)
                )
            elif search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department)
                )
        if search_by_category or select_by_category:
            if search_by_category and select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category) &
                    Q(category__id=select_by_category)
                )
            elif search_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category)
                )
            elif select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(category__id=select_by_category)
                )
        if select_by_country or search_by_country:
            if select_by_country and search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country) &
                    Q(country__id=select_by_country)
                )
            elif search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country)
                )
            elif select_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(skills__slug=self.kwargs.get('slug')) &
                    Q(country__id=select_by_country)
                )
        jobs_skills = jobs.JobsListings.objects.filter(skills__slug=self.kwargs.get('slug'))
        return jobs_skills

    def get_title(self):
        title = self.model.objects.get(slug=self.kwargs.get('slug'))
        return f'Jobs By {title.all_skills} Skill'


class JobsByCountryList(FilterContext, ContextData, ListView):
    model = accounts.CountryModel
    template_name = 'listings/joblistings.html'
    context_object_name = 'joblistings'
    paginate_by = 6

    def get_title(self):
        title = self.model.objects.get(slug=self.kwargs['slug'])
        return f'Jobs In {title.name}'

    def get_queryset(self):
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        if select_by_job_type:
            return jobs.JobsListings.objects.filter(
                Q(country__slug=self.kwargs.get('slug')) &
                Q(job_type__id=select_by_job_type)
            )
        if select_by_department or search_by_department:
            if select_by_department and search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(country__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department) &
                    Q(department__id__in=select_by_department)
                )
            elif select_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(country__slug=self.kwargs.get('slug')) &
                    Q(department__id__in=select_by_department)
                )
            elif search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(country__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department)
                )
        if select_by_skills:
            return jobs.JobsListings.objects.filter(
                Q(country__slug=self.kwargs.get('slug')) &
                Q(skills__id__in=select_by_skills)
            )
        if select_by_duration:
            return jobs.JobsListings.objects.filter(
                Q(country__slug=self.kwargs.get('slug')) &
                Q(duration__id=select_by_duration)
            )
        if search_by_category or select_by_category:
            if search_by_category and select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(country__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category) &
                    Q(category__id=select_by_category)
                )
            elif search_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(country__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category)
                )
            elif select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(country__slug=self.kwargs.get('slug')) &
                    Q(category__id=select_by_category)
                )
        else:
            return jobs.JobsListings.objects.filter(country__slug=self.kwargs.get('slug'))


class AccountsListView(ContextData, ListView):
    model = accounts.AccountType
    template_name = 'filters/all-accounts.html'
    context_object_name = "accounts"
    paginate_by = 6


class JobsByAccountList(FilterContext, ContextData, ListView):
    model = accounts.AccountType
    template_name = 'listings/joblistings.html'
    context_object_name = 'joblistings'
    paginate_by = 6

    def get_title(self):
        title = self.model.objects.get(slug=self.kwargs.get('slug'))
        return f'Jobs From {title.title} Account'

    def get_queryset(self):
        select_by_country = self.request.GET.get('select_by_country')
        search_by_country = self.request.GET.get('search_by_country')
        search_by_category = self.request.GET.get('search_by_category')
        select_by_category = self.request.GET.get('select_by_category')
        select_by_duration = self.request.GET.get('select_by_duration')
        select_by_skills = self.request.GET.getlist('select_by_skills')
        select_by_department = self.request.GET.getlist('select_by_department')
        search_by_department = self.request.GET.get('search_by_department')
        select_by_job_type = self.request.GET.get('select_by_job_type')
        if select_by_job_type:
            return jobs.JobsListings.objects.filter(
                Q(account_type__slug=self.kwargs.get('slug')) &
                Q(job_type__id=select_by_job_type)
            )
        if select_by_department or search_by_department:
            if select_by_department and search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department) &
                    Q(department__id__in=select_by_department)
                )
            elif select_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(department__id__in=select_by_department)
                )
            elif search_by_department:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(department__department__contains=search_by_department)
                )
        if select_by_skills:
            return jobs.JobsListings.objects.filter(
                Q(account_type__slug=self.kwargs.get('slug')) &
                Q(skills__id__in=select_by_skills)
            )
        if select_by_duration:
            return jobs.JobsListings.objects.filter(
                Q(account_type__slug=self.kwargs.get('slug')) &
                Q(duration__id=select_by_duration)
            )
        if search_by_category or select_by_category:
            if search_by_category and select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category) &
                    Q(category__id=select_by_category)
                )
            elif search_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(category__name__icontains=search_by_category)
                )
            elif select_by_category:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(category__id=select_by_category)
                )
        if select_by_country or search_by_country:
            if select_by_country and search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country) &
                    Q(country__id=select_by_country)
                )
            elif search_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(country__name__icontains=search_by_country)
                )
            elif select_by_country:
                return jobs.JobsListings.objects.filter(
                    Q(account_type__slug=self.kwargs.get('slug')) &
                    Q(country__id=select_by_country)
                )
        else:
            jobs_accounts = jobs.JobsListings.objects.filter(account_type__slug=self.kwargs.get('slug'))
            return jobs_accounts
