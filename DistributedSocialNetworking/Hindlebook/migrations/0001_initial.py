# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('tag', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, serialize=False, max_length=40, blank=True, primary_key=True)),
                ('text', models.CharField(max_length=2048)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForeignUser',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, serialize=False, max_length=40, blank=True, primary_key=True)),
                ('username', models.CharField(max_length=30, verbose_name='username')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(upload_to='')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('host', models.CharField(unique=True, max_length=100)),
                ('host_name', models.CharField(default='', unique=True, max_length=50, blank=True)),
                ('share_posts', models.BooleanField(default=True)),
                ('share_images', models.BooleanField(default=True)),
                ('require_auth', models.BooleanField(default=True)),
                ('password', models.CharField(default='', max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, serialize=False, max_length=40, blank=True, primary_key=True)),
                ('title', models.CharField(default='No title', max_length=40, blank=True)),
                ('description', models.CharField(default='No description', max_length=40, blank=True)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now_add=True)),
                ('source', models.CharField(default='Unknown source', max_length=100, blank=True)),
                ('origin', models.CharField(default='Unknown origin', max_length=100, blank=True)),
                ('content_type', models.CharField(default='text/plain', max_length=15)),
                ('privacy', models.IntegerField(default=5, choices=[(0, 'PUBLIC'), (1, 'FOAF'), (2, 'FRIENDS'), (3, 'PRIVATE'), (4, 'SERVERONLY')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('host', models.CharField(unique=True, max_length=100)),
                ('host_name', models.CharField(default='', unique=True, max_length=50, blank=True)),
                ('connection_limit', models.IntegerField(default=10, blank=True)),
                ('password', models.CharField(default='', max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('github_id', models.CharField(default='', max_length=30, blank=True)),
                ('about', models.CharField(default='', max_length=250, blank=True)),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=40, blank=True)),
                ('host', models.CharField(default='', max_length=100, blank=True)),
                ('follows', models.ManyToManyField(related_name='followed_by', to=settings.AUTH_USER_MODEL, blank=True)),
                ('follows_foreign', models.ManyToManyField(related_name='follows_foreign_rel_+', to=settings.AUTH_USER_MODEL, blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', related_name='user_set', blank=True)),
                ('server', models.ForeignKey(default=1, to='Hindlebook.Server', related_name='users', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_query_name='user', help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='tagged_posts', to='Hindlebook.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='attached_to',
            field=models.ForeignKey(to='Hindlebook.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foreignuser',
            name='node',
            field=models.ForeignKey(related_name='users', to='Hindlebook.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='foreign_author',
            field=models.ForeignKey(to='Hindlebook.ForeignUser', related_name='comments', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='Hindlebook.Post'),
            preserve_default=True,
        ),
    ]
