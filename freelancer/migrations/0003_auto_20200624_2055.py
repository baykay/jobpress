# Generated by Django 3.0.7 on 2020-06-24 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0002_auto_20200624_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancerprofile',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
