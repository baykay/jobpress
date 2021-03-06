# Generated by Django 3.0.7 on 2020-06-24 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0001_initial'),
        ('accounts', '0002_auto_20200624_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposals',
            name='freelancer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposals',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.JobsListings'),
        ),
        migrations.AddField(
            model_name='jobsreportedissues',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobsreportedissues',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_freelancer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobsreportedissues',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_job', to='jobs.JobsListings'),
        ),
        migrations.AddField(
            model_name='jobsreportedissues',
            name='logger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.AccountType'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobs', to='jobs.JobsCategories'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.CountryModel'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.DepartmentModel'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.DurationModel'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='hired_freelancer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hired_freelancer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.JobTypeModel'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='membership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.MembershipModel'),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='saves',
            field=models.ManyToManyField(related_name='saved_jobs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobslistings',
            name='skills',
            field=models.ManyToManyField(to='accounts.SkillModel'),
        ),
        migrations.AddField(
            model_name='joboffers',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='joboffers',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='joboffers',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobsListings'),
        ),
    ]
