from django.urls import path

from jobs import views

app_name = 'jobs'
urlpatterns = [
    path('', views.JobsListingsView.as_view(), name='all-jobs'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('followed-companies/', views.JobsByFollowedCompanies.as_view(), name='followed_companies'),
    path('jobpress-jobs/', views.BrowseAllJobs.as_view(), name='jobpress-jobs'),
    path('Job_offer/<username>', views.JobOfferView.as_view(), name='job_offer'),
    path('detail/<slug:slug>/', views.JobsDetailView.as_view(), name='job_detail'),
    path('make-proposal/<slug:slug>/', views.MakeProposalView.as_view(), name='make_proposal'),

    path('all-categories/', views.CategoriesListView.as_view(), name='all-categories'),
    path('categories/<slug:slug>/', views.JobsByCategoryList.as_view(), name='jobs_categories_list'),

    path('all-countries/', views.CountriesListView.as_view(), name='all-countries'),
    path('countries/<slug:slug>/', views.JobsByCountryList.as_view(), name='jobs_countries_list'),

    path('all-accounts/', views.AccountsListView.as_view(), name='all-accounts'),
    path('accounts/<slug:slug>/', views.JobsByAccountList.as_view(), name='jobs_accounts_list'),

    path('all-skills/', views.SkillsListView.as_view(), name='all-skills'),
    path('skills/<slug:slug>/', views.JobsBySkillsList.as_view(), name='jobs_skills_list'),

    path('all-departments/', views.DepartmentListView.as_view(), name='all-departments'),
    path('departments/<slug:slug>/', views.JobsByDepartmentsList.as_view(), name='jobs_department_list'),
]
