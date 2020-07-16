from django.urls import path
from pages.views import IndexView, AboutView, PrivacyPolicyView, ProcessView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('policy/', PrivacyPolicyView.as_view(), name='policy'),
    path('process/', ProcessView.as_view(), name='process'),
]
