from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.users_login_view, name='login'),
    path('details/', views.ChangeAccountDetails.as_view(), name='details'),
    path('delete_account/', views.accounts_delete_view, name='delete_account'),
    path('help_support/', views.HelpAndSupportView.as_view(), name='help_support'),
    path('create_support/', views.CreateHelpAndSupportView.as_view(), name='create_support'),
    path('email_notification/', views.EmailNotificationView.as_view(), name='email_notification'),
    path('account_settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('logout/', views.users_logout_view, name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('register/activate/<slug:uidb64>/<slug:token>/', views.account_activation_view, name='activate'),
    path('register/freelancer/', views.freelancer_signup_view, name='freelancer'),
    path('register/company/', views.company_signup_view, name='company'),
]
