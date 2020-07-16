from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import JobPressUserCreationForm, JobPressUserUpdateForm
Users = get_user_model()


class JobPressUsersAdmin(UserAdmin):
    add_form = JobPressUserCreationForm
    form = JobPressUserUpdateForm
    model = Users
    list_display = UserAdmin.list_display + ('is_company', 'is_freelancer')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_company', 'is_freelancer')}),
    )


admin.site.register(Users, JobPressUsersAdmin)
