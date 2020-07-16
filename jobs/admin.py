from django.contrib import admin

from jobs import models

admin.site.register(models.JobsListings)
admin.site.register(models.Proposals)
admin.site.register(models.JobOffers)
admin.site.register(models.JobsCategories)
