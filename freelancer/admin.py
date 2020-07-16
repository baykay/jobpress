from django.contrib import admin
from .models import FreelancerProfile, FreelancerProjects, FreelancerAwards, FreelancerSkills, FreelancerExperience, FreelancerEducation
# Register your models here.

admin.site.register(FreelancerEducation)
admin.site.register(FreelancerSkills)
admin.site.register(FreelancerProjects)
admin.site.register(FreelancerAwards)
admin.site.register(FreelancerExperience)
admin.site.register(FreelancerProfile)
