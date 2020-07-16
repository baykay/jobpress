from django.urls import path

from company import views as company

app_name = 'company'
urlpatterns = [
    path('all/', company.CompanyListView.as_view(), name='companies_list'),
    path('hire/', company.HireView.as_view(), name='hire'),
    path('completed-jobs/', company.CompletedJobs.as_view(), name='completed_jobs'),
    path('hired/<slug>/detail/', company.HireJobView.as_view(), name='hired_job_detail'),
    path('job_status_tracker', company.job_status_tracker, name='job_status_tracker'),
    path('hired-jobs/', company.HiredOnGoingJobs.as_view(), name='hired_on_going_jobs'),
    path('feedback/', company.Feedback.as_view(), name='feedback'),
    path('manage/', company.CompanyManageJobs.as_view(), name='manage_jobs'),
    path('detail/<slug:username>/', company.CompanyDetailView.as_view(), name='company_detail'),
    path('manage/update/<slug:slug>/', company.JobsUpdateView.as_view(), name='update_job'),
    path('manage/delete/<slug:slug>/', company.JobsDeleteView.as_view(), name='delete_job'),
    path('postjob/', company.JobCreateView.as_view(), name='postjob'),
    path('proposal/<slug:slug>/', company.ProposalsPerJobView.as_view(), name='per_job_proposals'),
    path('profile/', company.CompanyProfileView.as_view(), name='profile'),
    path('dashboard/', company.CompanyDashboard.as_view(), name='dashboard'),
    path('statistics/', company.CompanyStatistics.as_view(), name='statistics'),
]
