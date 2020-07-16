from django.urls import path
from freelancer import views

app_name = 'freelancer'
urlpatterns = [
    path('follow_route/', views.FollowCompanyView.as_view(), name='follow_route'),
    path('profile/', views.FreelancerProfileView.as_view(), name='profile'),
    path('dashboard/', views.FreelancerDashBoard.as_view(), name='dashboard'),
    path('save_job/', views.SaveJobToggle.as_view(), name='save_job'),
    path('followed-companies/', views.FollowedCompanies.as_view(), name='followed_companies'),
    path('saved-jobs-view/', views.SavedJobsView.as_view(), name='saved_job_view'),
    path('<username>/profile/', views.FreelancerDetailView.as_view(), name='detail'),
    path('by/<slug>/', views.SimilarFreelancerView.as_view(), name='similar_freelancers'),
    path('all/', views.FreelancerListView.as_view(), name='freelancer_list'),
    path('project/delete/<int:project_id>', views.project_delete_view, name='project_delete'),
    path('project/update/<int:project_id>', views.project_update_view, name='project_update'),
    path('skills/', views.skills_view, name='skills'),
    path('skill/delete/<int:skill_id>', views.skill_delete_view, name='skill_delete'),
    path('skill/update/<int:skill_id>', views.skill_update_view, name='skill_update'),
    path('projects/', views.projects_view, name='projects'),
    path('awards/', views.awards_view, name='awards'),
    path('experience/', views.experience_view, name='experience'),
    path('experience/delete/<int:experience_id>', views.experience_delete_view, name='experience_delete'),
    path('experience/update/<int:experience_id>', views.experience_update_view, name='experience_update'),
    path('education/delete/<int:education_id>', views.education_delete_view, name='education_delete'),
    path('education/update/<int:education_id>', views.education_update_view, name='education_update'),
    path('education/', views.education_view, name='education'),
    path('awards/delete/<int:pk>', views.award_delete_view, name='awards_delete'),
    path('awards/update/<int:pk>', views.award_update_view, name='awards_update'),
]

