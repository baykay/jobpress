from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, TemplateView, View

from accounts.models import SkillModel
from company.models import CompanyProfile
from freelancer import forms
from freelancer import models
from freelancer.models import FreelancerProfile
from jobs.models import JobsCategories, JobsListings, Proposals
from utilities.decorators import freelancer_required_view
from utilities.mixins import ContextData, FreelancerRequired

Users = get_user_model()


class FollowCompanyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        company_to_follow = request.POST.get('company_to_follow')
        request_freelancer = request.user
        CompanyProfile.objects.follow_company(company_to_follow, request_freelancer)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class FreelancerDashBoard(FreelancerRequired, TemplateView):
    template_name = 'freelancer_dashboard.html'
    model = JobsListings

    def get_jobs_completed(self):
        completed_jobs = self.model.objects.filter(
            Q(hired=True) &
            Q(proposed=True) &
            Q(completed=True) &
            Q(hired_freelancer=self.request.user)
        )
        return completed_jobs

    def get_users_jobs(self):
        jobs_hired = JobsListings.objects.filter(
            Q(hired=True) &
            Q(proposed=True) &
            Q(hired_freelancer=self.request.user)
        )
        return jobs_hired

    def jobs_earnings(self):
        jobs_earnings = Proposals.objects.filter(
            Q(job__hired=True) &
            Q(job__proposed=True) &
            Q(job__completed=True) &
            Q(freelancer=self.request.user)
        )
        return jobs_earnings

    def get_context_data(self, **kwargs):
        context = super(FreelancerDashBoard, self).get_context_data(**kwargs)
        context['hired_jobs'] = self.get_users_jobs()
        context['jobs_earnings'] = self.jobs_earnings()
        context['completed_jobs'] = self.get_jobs_completed()
        return context


class SavedJobsView(FreelancerRequired, ListView):
    template_name = 'save_items.html'
    context_object_name = 'saved_items'
    paginate_by = 8

    def get_queryset(self):
        request_freelancer = self.request.user
        job_ids = [job_id.id for job_id in request_freelancer.saved_jobs.all()]
        return JobsListings.objects.filter(id__in=job_ids)


class FollowedCompanies(FreelancerRequired, ListView):
    template_name = 'followed_companies.html'
    context_object_name = 'followed_companies'
    paginate_by = 5

    def get_queryset(self):
        request_freelancer = self.request.user
        company_ids = [company_id.user.id for company_id in request_freelancer.is_following.all()]
        return Users.objects.filter(id__in=company_ids)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FollowedCompanies, self).get_context_data(**kwargs)
        context['followed_companies_count'] = self.get_queryset()
        return context


class SaveJobToggle(FreelancerRequired, View):
    def post(self, request, *args, **kwargs):
        from freelancer.models import FreelancerProfile
        job_to_save = request.POST.get('job_to_save')
        request_freelancer = request.user
        FreelancerProfile.objects.save_job(job_to_save, request_freelancer)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class SimilarFreelancerView(ContextData, ListView):
    model = Users
    template_name = 'freelancers_by_interests.html'
    context_object_name = 'search_queryset'
    paginate_by = 6

    def get_queryset(self):
        return self.model.objects.filter(freelancer_profile__interests__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SimilarFreelancerView, self).get_context_data(**kwargs)
        context['query'] = get_object_or_404(JobsCategories, slug=self.kwargs['slug'])
        context['total_count'] = self.get_queryset()
        return context


class FreelancerDetailView(ContextData, DetailView):
    model = Users
    template_name = 'freelancer_detail.html'
    slug_url_kwarg = 'username'
    context_object_name = 'freelancer'

    def get_object(self, queryset=None):
        return get_object_or_404(Users, is_freelancer=True, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super(FreelancerDetailView, self).get_context_data(**kwargs)
        return context


class FreelancerListView(ContextData, ListView):
    template_name = 'freelancer_list.html'
    model = FreelancerProfile
    context_object_name = 'freelancers'
    paginate_by = 8
    title = 'All Freelancers'

    def get_queryset(self):
        freelancer_by_hourly_rate = self.request.GET.get('freelancer_by_hourly_rate')
        freelancer_by_profession = self.request.GET.get('freelancer_by_profession')
        freelancer_by_department = self.request.GET.get('freelancer_by_department')
        freelancer_by_account_type = self.request.GET.get('freelancer_by_account_type')
        search_freelancer_by_interests = self.request.GET.get('search_freelancer_by_interests')
        select_freelancer_by_interests = self.request.GET.getlist('select_freelancer_by_interests')
        freelancer_by_country = self.request.GET.get('freelancer_by_country')
        if freelancer_by_hourly_rate:
            print(freelancer_by_hourly_rate)
            gt_hire_rate = freelancer_by_hourly_rate.split('-')[0]
            lt_hire_rate = freelancer_by_hourly_rate.split('-')[1]
            return self.model.objects.filter(
                Q(hire_rate__gte=gt_hire_rate) &
                Q(hire_rate__lte=lt_hire_rate)
            )
        if search_freelancer_by_interests or select_freelancer_by_interests:
            if search_freelancer_by_interests and select_freelancer_by_interests:
                return self.model.objects.filter(
                    Q(interests__id__in=select_freelancer_by_interests) &
                    Q(interests__name__icontains=search_freelancer_by_interests)
                )
            elif search_freelancer_by_interests:
                return self.model.objects.filter(
                    Q(interests__name__icontains=search_freelancer_by_interests)
                )
            elif select_freelancer_by_interests:
                return self.model.objects.filter(
                    Q(interests__id__in=select_freelancer_by_interests)
                )
        if freelancer_by_account_type:
            return self.model.objects.filter(
                Q(account_type__id=freelancer_by_account_type)
            )
        if freelancer_by_department:
            return self.model.objects.filter(
                Q(department__id=freelancer_by_department)
            )
        if freelancer_by_profession:
            return self.model.objects.filter(
                Q(profession__icontains=freelancer_by_profession)
            )
        if freelancer_by_country:
            return self.model.objects.filter(
                Q(country__id=freelancer_by_country)
            )
        else:
            return self.model.objects.filter(user__is_active=True, user__is_freelancer=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['freelancer_filter_form'] = forms.FreelancerFilterForm(self.request.GET)
        context['freelancer_by_hourly_rate'] = self.request.GET.get('freelancer_by_hourly_rate')
        context['freelancer_by_profession'] = self.request.GET.get('freelancer_by_profession')
        context['freelancer_by_department'] = self.request.GET.get('freelancer_by_department')
        context['freelancer_by_account_type'] = self.request.GET.get('freelancer_by_account_type')
        context['search_freelancer_by_interests'] = self.request.GET.get('search_freelancer_by_interests')
        context['select_freelancer_by_interests'] = self.request.GET.getlist('select_freelancer_by_interests')
        context['freelancer_by_country'] = self.request.GET.get('freelancer_by_country')
        return context


class FreelancerProfileView(FreelancerRequired, UpdateView):
    model = models.FreelancerProfile
    form_class = forms.FreelancerProfileForm
    template_name = 'freelancer_profile.html'
    success_url = reverse_lazy('freelancer:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Profile updated successfully')
        return super(FreelancerProfileView, self).form_valid(form)

    def get_object(self, queryset=None):
        queryset = self.request.user.freelancer_profile
        return queryset


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def projects_view(request):
    freelancer = request.user
    if request.method == 'POST':
        form = forms.FreelancerProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            image = form.cleaned_data['image']

            if not name:
                messages.error(request, 'You must provide a name for your project')
                return redirect('freelancer:projects')
            else:
                if not image:
                    messages.error(request, 'You must provide an image for your project')
                    return redirect('freelancer:projects')
                else:
                    models.FreelancerProjects.objects.create(name=name, image=image, url=url, freelancer=freelancer)
                    messages.success(request, 'Project added successfully')
                    return redirect('freelancer:projects')
    else:
        form = forms.FreelancerProjectsForm()
    projects = models.FreelancerProjects.objects.filter(freelancer=freelancer)
    context = {
        'form': form,
        'projects': projects
    }
    return render(request, 'freelancer_projects.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def project_delete_view(request, project_id):
    project = get_object_or_404(models.FreelancerProjects, id=project_id)
    if project.freelancer != request.user:
        messages.error(request, 'Cant be deleted, by you...')
        return redirect('freelancer:projects')
    else:
        project.delete()
        messages.success(request, 'Deleted {} successfully'.format(project.name))
    return redirect(reverse('freelancer:projects'))


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def project_update_view(request, project_id):
    project = get_object_or_404(models.FreelancerProjects, id=project_id)
    if project.freelancer != request.user:
        messages.error(request, 'Cant be updated, by you...')
        return redirect('freelancer:projects')
    if request.method == 'POST':
        form = forms.FreelancerProjectsForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated "{}" successfully'.format(form.cleaned_data['name']))
            return redirect('freelancer:projects')
    else:
        form = forms.FreelancerProjectsForm(instance=project)
    return render(request, 'freelancer_projects.html', {'form': form})


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def awards_view(request):
    freelancer = request.user
    if request.method == 'POST':
        form = forms.FreelancerAwardForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            award_date = form.cleaned_data['award_date']
            image = form.cleaned_data['image']

            if not title:
                messages.error(request, 'You must provide a title for your award')
                return redirect('freelancer:awards')
            else:
                if not image:
                    messages.error(request, 'You must provide an image for your award')
                    return redirect('freelancer:awards')
                else:
                    if not award_date:
                        messages.error(request, 'You must provide a date you received your award')
                    else:
                        models.FreelancerAwards.objects.create(title=title, image=image, award_date=award_date,
                                                               freelancer=freelancer)
                        messages.success(request, 'Award added successfully')
                        return redirect('freelancer:awards')
    else:
        form = forms.FreelancerAwardForm()
    awards = models.FreelancerAwards.objects.filter(freelancer=freelancer)
    context = {
        'form': form,
        'awards': awards
    }
    return render(request, 'freelancer_awards.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def award_delete_view(request, pk):
    award = get_object_or_404(models.FreelancerAwards, pk=pk)
    if award.freelancer != request.user:
        messages.error(request, 'Cant be deleted by you')
    else:
        award.delete()
        messages.info(request, 'You have deleted "{}"'.format(award.title))
        return redirect('freelancer:awards')


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def award_update_view(request, pk):
    award = get_object_or_404(models.FreelancerAwards, pk=pk)
    if award.freelancer != request.user:
        messages.error(request, 'Cant be updated by you')
        redirect('freelancer:awards')
    else:
        if request.method == 'POST':
            form = forms.FreelancerAwardForm(request.POST, request.FILES, instance=award)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated Successfully')
                return redirect('freelancer:awards')
    form = forms.FreelancerAwardForm(instance=award)
    context = {
        'form': form
    }
    return render(request, 'freelancer_awards.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def skills_view(request):
    freelancer = request.user
    if request.method == 'POST':
        form = forms.FreelancerSkillsForm(request.POST)
        if form.is_valid():
            selected_skill = form.cleaned_data['all_skills']
            title = form.cleaned_data['title']
            rate = form.cleaned_data['rate']
            if not title and selected_skill is not None:
                models.FreelancerSkills.objects.create(title=selected_skill, freelancer=freelancer, rate=rate)
                messages.success(request, 'Added Successfully')
                return redirect('freelancer:skills')
            else:
                if title and selected_skill is None:
                    SkillModel.objects.get_or_create(all_skills=title)
                    check_title = models.FreelancerSkills.objects.filter(title=title)
                    if check_title.exists():
                        pass
                        messages.info(request, 'This skill you provided already exists, select it...')
                    else:
                        models.FreelancerSkills.objects.create(title=title, freelancer=freelancer, rate=rate)
                        messages.success(request, 'Added Successfully')
                        return redirect('freelancer:skills')
                else:
                    if title and selected_skill:
                        SkillModel.objects.get_or_create(all_skills=title)
                        check_title = models.FreelancerSkills.objects.filter(title=title)
                        if check_title.exists():
                            pass
                            messages.info(request, 'This skill you provided already exists, select it...')
                        else:
                            models.FreelancerSkills.objects.create(title=title, freelancer=freelancer, rate=rate)
                            models.FreelancerSkills.objects.create(title=selected_skill, freelancer=freelancer,
                                                                   rate=rate)
                            messages.success(request, 'Added Successfully')
                            return redirect('freelancer:skills')
                    else:
                        if not title and not selected_skill:
                            messages.warning(request, 'You have to provide a skill or select one')
                            return redirect('freelancer:skills')

    else:
        form = forms.FreelancerSkillsForm()
    skills = models.FreelancerSkills.objects.filter(freelancer=freelancer)
    context = {
        'form': form,
        'skills': skills
    }
    return render(request, 'freelancer_skill.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def skill_delete_view(request, skill_id):
    skill = get_object_or_404(models.FreelancerSkills, id=skill_id)
    if skill.freelancer != request.user:
        messages.error(request, 'This skill cant be deleted by you')
        return redirect('freelancer:skills')
    else:
        skill.delete()
        messages.info(request, 'you have deleted this skill "{}"'.format(skill.title))
        return redirect('freelancer:skills')


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def skill_update_view(request, skill_id):
    skill = get_object_or_404(models.FreelancerSkills, id=skill_id)
    if skill.freelancer != request.user:
        messages.warning(request, 'You cant update this skill')
        return redirect('freelancer:skills')
    if request.method == 'POST':
        form = forms.FreelancerSkillsForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('freelancer:skills')
    else:
        form = forms.FreelancerSkillsForm(instance=skill)

    context = {
        'form': form
    }
    return render(request, 'freelancer_skill.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def experience_view(request):
    freelancer = request.user
    if request.method == 'POST':
        form = forms.FreelancerExperienceForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            company = form.cleaned_data['company']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if not title:
                messages.warning(request, 'You must provide a title')
                return redirect('freelancer:experience')
            if not company:
                messages.warning(request, 'You must provide a company')
                return redirect('freelancer:experience')
            if not description:
                messages.warning(request, 'You must provide a description')
                return redirect('freelancer:experience')
            if not start_date:
                messages.warning(request, 'You must provide a start date')
                return redirect('freelancer:experience')
            if not end_date:
                pass
            models.FreelancerExperience.objects.create(
                freelancer=freelancer, title=title, company=company, description=description, start_date=start_date,
                end_date=end_date)
            messages.success(request, 'Added Successfully')
            return redirect('freelancer:experience')
    else:
        form = forms.FreelancerExperienceForm()
    experiences = models.FreelancerExperience.objects.filter(freelancer=freelancer)
    context = {
        'form': form,
        'experiences': experiences
    }
    return render(request, 'freelancer_experience.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def experience_update_view(request, experience_id):
    experience = get_object_or_404(models.FreelancerExperience, id=experience_id)
    if experience.freelancer != request.user:
        messages.error(request, 'This cant be updated by you')
    if request.method == 'POST':
        form = forms.FreelancerExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            title = form.cleaned_data['title']
            company = form.cleaned_data['company']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if not title:
                messages.warning(request, 'You must provide a title')
                return redirect('freelancer:experience')
            if not company:
                messages.warning(request, 'You must provide a company')
                return redirect('freelancer:experience')
            if not description:
                messages.warning(request, 'You must provide a description')
                return redirect('freelancer:experience')
            if not start_date:
                messages.warning(request, 'You must provide a start date')
                return redirect('freelancer:experience')
            if not end_date:
                pass
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('freelancer:experience')
    else:
        form = forms.FreelancerExperienceForm(instance=experience)
    context = {
        'form': form,
    }
    return render(request, 'freelancer_experience.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def experience_delete_view(request, experience_id):
    experience = get_object_or_404(models.FreelancerExperience, id=experience_id)
    if experience.freelancer != request.user:
        messages.error(request, 'This experience cant be deleted by you')
        return redirect('freelancer:experience')
    else:
        experience.delete()
        messages.info(request, 'you have deleted this experience "{}"'.format(experience.title))
        return redirect('freelancer:experience')


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def education_view(request):
    freelancer = request.user
    if request.method == 'POST':
        form = forms.FreelancerEducationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            institution = form.cleaned_data['institution']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if not title:
                messages.warning(request, 'You must provide a title')
                return redirect('freelancer:education')
            if not institution:
                messages.warning(request, 'You must provide a institute')
                return redirect('freelancer:education')
            if not description:
                messages.warning(request, 'You must provide a description')
                return redirect('freelancer:education')
            if not start_date:
                messages.warning(request, 'You must provide a start date')
                return redirect('freelancer:education')
            if not end_date:
                pass
            models.FreelancerEducation.objects.create(
                freelancer=freelancer, title=title, institution=institution, description=description,
                start_date=start_date, end_date=end_date
            )
            messages.success(request, 'Added Successfully')
            return redirect('freelancer:education')
    else:
        form = forms.FreelancerEducationForm()
    education = models.FreelancerEducation.objects.filter(freelancer=freelancer)
    context = {
        'form': form,
        'educations': education
    }
    return render(request, 'freelancer_education.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def education_update_view(request, education_id):
    education = get_object_or_404(models.FreelancerEducation, id=education_id)
    if education.freelancer != request.user:
        messages.error(request, 'This cant be updated by you')
        return redirect('freelancer:education')
    if request.method == 'POST':
        form = forms.FreelancerEducationForm(request.POST, instance=education)
        if form.is_valid():
            title = form.cleaned_data['title']
            institution = form.cleaned_data['institution']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if not title:
                messages.warning(request, 'You must provide a title')
                return redirect('freelancer:experience')
            if not institution:
                messages.warning(request, 'You must provide a institution')
                return redirect('freelancer:experience')
            if not description:
                messages.warning(request, 'You must provide a description')
                return redirect('freelancer:education')
            if not start_date:
                messages.warning(request, 'You must provide a start date')
                return redirect('freelancer:education')
            if not end_date:
                pass
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('freelancer:education')
    else:
        form = forms.FreelancerEducationForm(instance=education)
    context = {
        'form': form,
    }
    return render(request, 'freelancer_education.html', context)


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
@method_decorator(freelancer_required_view)
def education_delete_view(request, education_id):
    education = get_object_or_404(models.FreelancerEducation, id=education_id)
    if education.freelancer != request.user:
        messages.error(request, 'This cant be deleted by you')
        return redirect('freelancer:education')
    else:
        education.delete()
        messages.info(request, 'you have deleted "{}"'.format(education.title))
        return redirect('freelancer:education')
