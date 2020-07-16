from django.utils.decorators import method_decorator

from accounts import forms
from accounts import models as accounts_model
from company.models import CompanyProfile
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from freelancer.models import FreelancerProfile
from utilities.mixins import ContextData
from utilities.token import account_activation_token

User = get_user_model()


class CreateHelpAndSupportView(LoginRequiredMixin, CreateView):
    model = accounts_model.HelpAndSupportModel
    form_class = forms.AskHelpAndSupportForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateHelpAndSupportView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Query Posted!')
        return reverse('accounts:help_support')


class HelpAndSupportView(ListView):
    model = accounts_model.HelpAndSupportModel
    template_name = 'help_and_support.html'
    context_object_name = 'help'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(HelpAndSupportView, self).get_context_data(**kwargs)
        context['form'] = forms.AskHelpAndSupportForm(self.request.POST)
        return context

    def get_queryset(self):
        return self.model.objects.filter(answer__isnull=False)


class AccountSettingsView(LoginRequiredMixin, UpdateView):
    model = accounts_model.AccountSettingsModel
    template_name = 'account_settings.html'
    form_class = forms.AccountSettingsForm

    def get_object(self, queryset=None):
        return self.request.user.account_settings

    def get_success_url(self):
        messages.success(self.request, 'Your account was updated successfully...')
        return reverse('index')


class EmailNotificationView(LoginRequiredMixin, UpdateView):
    model = accounts_model.EmailNotificationModel
    form_class = forms.EmailNotificationForm
    template_name = 'email_notification.html'

    def get_object(self, queryset=None):
        return self.request.user.email_notification

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
def accounts_delete_view(request):
    if request.method == 'POST':
        form = forms.DeletedAccountsForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            reason = form.cleaned_data['reason']
            description = form.cleaned_data['description']
            unsubscribe = form.cleaned_data['unsubscribe']
            user_email = request.user.email
            user = authenticate(email=user_email, password=password)
            if user:
                accounts_model.DeletedAccountsModel.objects.create(
                    user_email=user_email, reason=reason, description=description)
                if unsubscribe:
                    no_email = accounts_model.EmailNotificationModel.objects.get(user=request.user)
                    no_email.delete()
                user_to_delete = request.user
                user_to_delete.delete()
                logout(request)
                messages.success(request, 'Your account has been deleted...')
                return redirect('index')
            else:
                messages.error(request, 'Invalid Password')
    else:
        form = forms.DeletedAccountsForm()
    context = {'form': form}
    return render(request, 'delete_account.html', context)


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    form_class = forms.ChangePasswordForm

    def get_success_url(self):
        return reverse('accounts:login')


class ChangeAccountDetails(LoginRequiredMixin, UpdateView):
    template_name = 'change_account_details.html'
    model = User
    form_class = forms.AccountDetailsForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'You have successfully updated your account info')
        return reverse('index')

    def form_valid(self, form):
        form.instance = self.request.user
        return super(ChangeAccountDetails, self).form_valid(form)


def account_activation_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        if user.is_company:
            company = CompanyProfile.objects.create(user=user)
            company.confirmed = True
            company.save()
        else:
            freelancer = FreelancerProfile.objects.create(user=user)
            freelancer.confirmed = True
            freelancer.save()
        messages.success(request, 'Your account confirmation was successful, kindly provide your profile information')
        if user.is_company:
            return redirect('company:profile')
        elif user.is_freelancer:
            return redirect('freelancer:profile')
    else:
        messages.error(
            request, 'Sorry your confirmation link is invalid, kindly request a new one')
        return render(request, 'authentication/email_confirmation_page.html')


def company_signup_view(request):
    if request.method == 'POST':
        form = forms.CompanyRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            unique_id = form.cleaned_data['username']
            if password == password2:
                is_already_been_used = User.objects.filter(email=email).exists()
                if is_already_been_used:
                    messages.error(request, 'Email is already been used')
                    return redirect('accounts:company')
                else:
                    username = unique_id
                    user = User(email=email, username=username)
                    user.set_password(password)
                    user.is_company = True
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)
                    email_subject = 'Your JobPress Email Confirmation Link'
                    email_message = render_to_string(
                        'authentication/account_activation_mail.html',
                        {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        }
                    )
                    recipients_email = email
                    send_email = EmailMessage(
                        email_subject, email_message, to=[recipients_email]
                    )
                    send_email.send()
                    messages.success(request, 'Account created successfully, kindly check your mail to '
                                              'confirm your account')
                    return redirect('accounts:company')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('accounts:company')
    else:
        form = forms.CompanyRegistrationForm()
    context = {'form': form}
    return render(request, 'authentication/register_as_company.html', context)


def freelancer_signup_view(request):
    # checking if the request method is post
    if request.method == 'POST':
        # if its a post request, get the fields from the html form
        form = forms.FreelancerRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            # then check if the fields are valid
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already been used')
                    return redirect('accounts:freelancer')
                else:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Username is already been used')
                        return redirect('accounts:freelancer')
                    else:
                        # create the user if the fields are valid using the  provided fields
                        user = User(username=username, email=email)
                        user.set_password(password)
                        user.is_freelancer = True
                        user.is_active = False
                        user.save()

                        # configurations for email confirmation
                        current_site = get_current_site(request)
                        email_subject = 'Your JobPress Email Confirmation Link'
                        email_message = render_to_string(
                            'authentication/account_activation_mail.html',
                            {
                                'user': user, 'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                            }
                        )
                        recipients_email = email
                        send_email = EmailMessage(email_subject, email_message, to=[recipients_email])
                        send_email.send()
                        messages.success(request, 'Account created successfully, kindly check your mail to '
                                                  'confirm your account')
                        return redirect('accounts:freelancer')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('accounts:freelancer')
    else:
        form = forms.FreelancerRegistrationForm()
    context = {'form': form}
    return render(request, 'authentication/register_as_freelancer.html', context)


class RegistrationView(ContextData, TemplateView):
    template_name = 'authentication/register.html'


def users_login_view(request):
    if request.method == 'POST':
        form = forms.UsersLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # messages.success(request, 'login successfully')
                    if user.is_company:
                        return redirect('company:statistics')
                    else:
                        return redirect('freelancer:dashboard')
                else:
                    messages.error(request, 'Sorry you haven\'t confirmed your account')
                    return redirect('accounts:login')
            else:
                messages.error(request, 'invalid credentials provided')
                return redirect('accounts:login')
    else:
        form = forms.UsersLoginForm()
    context = {'form': form}
    return render(request, 'authentication/login.html', context)


def users_logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('index')
