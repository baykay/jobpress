from django.contrib import admin
from accounts import models
# Register your models here.
admin.site.register(models.SkillModel)
admin.site.register(models.AccountType)
admin.site.register(models.CountryModel)
admin.site.register(models.GenderModel)
admin.site.register(models.DepartmentModel)
admin.site.register(models.AttachmentModel)
admin.site.register(models.MembershipModel)
admin.site.register(models.JobTypeModel)
admin.site.register(models.DurationModel)
admin.site.register(models.EmailNotificationModel)
admin.site.register(models.DeletedAccountsModel)
admin.site.register(models.AccountSettingsModel)
admin.site.register(models.HelpAndSupportModel)
admin.site.register(models.HelpAndSupportType)
