from django.shortcuts import render
from django.views.generic import TemplateView

from jobs import models as jobs
from accounts import  models as accounts
from utilities.mixins import ContextData


class IndexView(ContextData, TemplateView):
    template_name = 'site_pages/index.html'


class AboutView(ContextData, TemplateView):
    template_name = 'site_pages/about.html'



class ProcessView(ContextData, TemplateView):
    template_name = 'site_pages/howitworks.html'


class PrivacyPolicyView(ContextData, TemplateView):
    template_name = 'site_pages/privacypolicy.html'
