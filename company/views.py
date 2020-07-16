from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from company.forms import CompanyUpdateForm, HiredJobProposalStatus, JobsReportedIssuesForm, FeedbackForm
from company.models import CompanyProfile
from freelancer.models import FeedBackModel
from jobs.forms import JobsForm
from jobs.models import JobsListings, Proposals
from utilities.decorators import company_required_view
from utilities.mixins import ContextData, CompanyRequired

Users = get_user_model()


class CompanyStatistics(LoginRequiredMixin, CompanyRequired, TemplateView):
    template_name = 'company_statistics.html'

    def get_hired_freelancers(self):
        return Proposals.objects.filter(
            Q(job__company=self.request.user) &
            Q(job__hired=True) &
            Q(job__proposed=True)
        )

    def get_company(self):
        return self.request.user

    def get_completed_jobs(self):
        return JobsListings.objects.filter(
            Q(company=self.get_company()) &
            Q(hired=True) &
            Q(proposed=True) &
            Q(completed=True)
        )

    def get_on_going_jobs(self):
        return JobsListings.objects.filter(
            Q(company=self.get_company()) &
            Q(hired=True) &
            Q(proposed=True)
        )

    def get_context_data(self, **kwargs):
        context = super(CompanyStatistics, self).get_context_data(**kwargs)
        context['hired_freelancers'] = self.get_hired_freelancers()
        context['total_jobs'] = self.get_total_jobs()
        context['on_going_jobs'] = self.get_on_going_jobs()
        context['completed_jobs'] = self.get_completed_jobs()
        return context

    def get_total_jobs(self):
        return JobsListings.objects.filter(company=self.get_company())


class Feedback(CompanyRequired, CreateView):
    model = FeedBackModel
    context_object_name = 'feedback'
    template_name = 'feedback.html'
    form_class = FeedbackForm


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(company_required_view)
def job_status_tracker(request, **kwargs):
    if request.method == 'POST':
        issue = request.POST.get('issue')
        attachment = request.POST.get('attachment')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class HireJobView(LoginRequiredMixin, CompanyRequired, View):
    def post(self, request, *args, **kwargs):
        hired_job = get_object_or_404(JobsListings, company=request.user, slug=kwargs.get('slug'))
        hired_job_proposal = get_object_or_404(Proposals, job=hired_job, freelancer=hired_job.hired_freelancer)
        status_form = HiredJobProposalStatus(request.POST)
        if status_form.is_valid():
            status = request.POST.get('status')
            if status == 'completed':
                hired_job.completed = True
                hired_job.hired = False
                hired_job.pending = False
                hired_job.proposed = False
                hired_job.save()
                messages.success(request, f'You have marked {hired_job} as completed.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        context = {
            'hired_job': hired_job,
            'status_form': status_form,
            'issue_form': JobsReportedIssuesForm(),
            'hired_job_proposal': hired_job_proposal,
        }
        return render(request, 'dashboard-hired-job-detail.html', context)

    def get(self, request, *args, **kwargs):
        hired_job = get_object_or_404(JobsListings, company=request.user, slug=kwargs.get('slug'))
        hired_job_proposal = get_object_or_404(Proposals, job=hired_job, freelancer=hired_job.hired_freelancer)
        status_form = HiredJobProposalStatus(request.POST)
        context = {
            'hired_job': hired_job,
            'status_form': status_form,
            'issue_form': JobsReportedIssuesForm(),
            'hired_job_proposal': hired_job_proposal,
        }
        return render(request, 'dashboard-hired-job-detail.html', context)


# @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
# @method_decorator(company_required_view)
# def hired_job_view(request, *args, **kwargs):
#     hired_job = get_object_or_404(JobsListings, company=request.user, slug=kwargs.get('slug'))
#     hired_job_proposal = get_object_or_404(Proposals, job=hired_job, freelancer=hired_job.hired_freelancer)
#     if request.method == 'POST':
#         status_form = HiredJobProposalStatus(request.POST)
#         if status_form.is_valid():
#             status = request.POST.get('status')
#             if status == 'completed':
#                 hired_job.completed = True
#                 hired_job.hired = False
#                 hired_job.pending = False
#                 hired_job.proposed = False
#                 hired_job.save()
#                 messages.success(request, f'You have marked {hired_job} as completed.')
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     else:
#         status_form = HiredJobProposalStatus()
#
#     context = {
#         'hired_job': hired_job,
#         'status_form': status_form,
#         'issue_form': JobsReportedIssuesForm(),
#         'hired_job_proposal': hired_job_proposal,
#     }
#     return render(request, 'dashboard-hired-job-detail.html', context)


class HiredOnGoingJobs(LoginRequiredMixin, CompanyRequired, ListView):
    template_name = 'dashboard-on-going-job.html'
    context_object_name = 'hired_jobs'

    def get_queryset(self):
        return JobsListings.objects.filter(company=self.request.user, hired=True)


class CompletedJobs(LoginRequiredMixin, CompanyRequired, ListView):
    template_name = 'dashboard-completed-jobs.html'
    context_object_name = 'completed_jobs'

    def get_queryset(self):
        return JobsListings.objects.filter(company=self.request.user, completed=True)


class HireView(LoginRequiredMixin, CompanyRequired, View):
    def post(self, request, *args, **kwargs):
        freelancer_username = request.POST.get('freelancer_username')
        job_slug = request.POST.get('job_slug')
        freelancer = get_object_or_404(Users, username__iexact=freelancer_username)
        job = get_object_or_404(JobsListings, company=request.user, slug__iexact=job_slug)
        if freelancer and job:
            if job.hired and job.hired_freelancer != freelancer:
                messages.info(request, 'You have already hired a freelancer for this job.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            # if job.hired and job.hired_freelancer == freelancer:
            #     messages.info(request, f'You have already hired {freelancer.freelancer_profile.get_full_name} for '
            #                            f'this job.')
            #     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            job.hired = True
            job.hired_freelancer = freelancer
            job.hired = True
            job.save()
            # delete_proposal = get_object_or_404(Proposals, job=job, freelancer=freelancer)
            # if delete_proposal:
            #     delete_proposal.delete()

            subject = 'Congratulations! You Are Hired.'
            current_site = get_current_site(request)
            email_message = render_to_string(
                'hire_email_notification.html',
                {
                    'job': job,
                    'freelancer': freelancer,
                    'domain': current_site.domain,
                }
            )
            freelancer_email = freelancer.email
            send_email = EmailMessage(
                subject, email_message, to=[freelancer_email]
            )
            send_email.send()

            messages.success(request, f'You have hired {freelancer.freelancer_profile.get_full_name} for {job.title}')
            # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            return redirect('company:hired_job_detail', slug=job_slug)


class ProposalsPerJobView(LoginRequiredMixin, CompanyRequired, ListView):
    model = Proposals
    template_name = 'per_job_proposals.html'
    context_object_name = 'proposals'
    paginate_by = 5

    def get_queryset(self):
        proposals = self.model.objects.filter(job__company_id=self.request.user.id, job__slug=self.kwargs['slug'])
        return proposals

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProposalsPerJobView, self).get_context_data(**kwargs)
        context['proposed_job'] = get_object_or_404(JobsListings, company=self.request.user, slug=self.kwargs['slug'])
        return context


class CompanyManageJobs(LoginRequiredMixin, CompanyRequired, ListView):
    template_name = 'dashboard-manage-jobs.html'
    context_object_name = 'jobs'
    model = JobsListings
    paginate_by = 10

    def get_queryset(self):
        return JobsListings.objects.filter(company=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyManageJobs, self).get_context_data(**kwargs)
        context['company_name'] = self.request.user.company_profile.name
        return context


class JobCreateView(LoginRequiredMixin, CompanyRequired, CreateView):
    template_name = 'crud/Job_form.html'
    model = JobsListings
    form_class = JobsForm

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)


class JobsUpdateView(LoginRequiredMixin, CompanyRequired, UpdateView):
    template_name = 'crud/Job_form.html'
    model = JobsListings
    form_class = JobsForm

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(JobsListings, company=self.request.user, slug=self.kwargs['slug'])


class JobsDeleteView(LoginRequiredMixin, CompanyRequired, DeleteView):
    template_name = 'crud/confirm_delete.html'
    model = JobsListings
    success_url = reverse_lazy('company:manage_jobs')

    def get_object(self, queryset=None):
        return get_object_or_404(JobsListings, company=self.request.user, slug=self.kwargs['slug'])


class CompanyProfileView(LoginRequiredMixin, CompanyRequired, UpdateView):
    model = CompanyProfile
    form_class = CompanyUpdateForm
    template_name = 'company_profile.html'
    success_url = reverse_lazy('company:statistics')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Profile updated successfully')
        return super(CompanyProfileView, self).form_valid(form)

    def get_object(self, queryset=None):
        queryset = self.request.user.company_profile
        return queryset


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(company_required_view)
def company_dashboard_profile(request):
    if request.method == 'POST':
        form = CompanyUpdateForm(
            request.POST, request.FILES, instance=request.user.company_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('company:statistics')
    else:
        form = CompanyUpdateForm(instance=request.user.company_profile)

    context = {'form': form}
    return render(request, 'company_profile.html', context)


class CompanyDashboard(LoginRequiredMixin, CompanyRequired, ListView):
    template_name = 'company_jobs.html'
    model = JobsListings
    context_object_name = 'company_jobs'
    paginate_by = 3

    def get_queryset(self):
        return JobsListings.objects.filter(company__exact=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyDashboard, self).get_context_data(**kwargs)
        context['company_jobs'] = self.get_queryset()
        return context


class CompanyListView(ContextData, ListView):
    model = CompanyProfile
    template_name = 'companieslist.html'
    context_object_name = 'companies'
    paginate_by = 8
    title = 'Companies in JobPress'

    def get_queryset(self):
        return self.model.objects.filter(user__is_company=True, user__is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class CompanyDetailView(ContextData, DetailView):
    template_name = 'companydetail.html'
    model = Users
    context_object_name = 'company'
    slug_url_kwarg = 'username'
    paginate_by = 6

    def get_object(self, queryset=None):
        return get_object_or_404(Users, is_company=True, username=self.kwargs['username'])

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['jobs'] = JobsListings.objects.filter(company__username__exact=self.kwargs['username'])
        return context
