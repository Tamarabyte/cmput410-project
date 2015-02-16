# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Hindlebook', '0003_auto_20150216_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('github_id', models.CharField(null=True, max_length=30)),
                ('join_date', models.DateField(verbose_name='date joined', auto_now_add=True)),
                ('profile_image', models.ImageField(null=True, upload_to='', blank=True)),
                ('follows', models.ManyToManyField(related_name='followed_by', to='Hindlebook.Author', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='Hindlebook.Author'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
