# Generated by Django 3.0.7 on 2020-07-04 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_articlecommentsmodel_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecommentsmodel',
            name='reply',
        ),
        migrations.CreateModel(
            name='ReplyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.ArticleCommentsModel')),
            ],
        ),
    ]
