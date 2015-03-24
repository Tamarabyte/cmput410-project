# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Hindlebook.models.validators
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('about', models.CharField(max_length=250, default='', blank=True)),
                ('uuid', models.CharField(serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, default=uuid.uuid4, primary_key=True, blank=True)),
                ('username', models.CharField(max_length=30, verbose_name='username')),
                ('github_id', models.CharField(max_length=30, default='', blank=True)),
                ('avatar', models.ImageField(default='default_avatar.jpg', upload_to='', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('follows', models.ManyToManyField(related_name='followed_by', to='Hindlebook.Author', db_index=True, blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_of', to='Hindlebook.Author', db_index=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('tag', models.CharField(max_length=25, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('guid', models.CharField(serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, default=uuid.uuid4, primary_key=True, blank=True)),
                ('comment', models.CharField(max_length=2048)),
                ('pubDate', models.DateTimeField(auto_now_add=True, verbose_name='date published', db_index=True)),
                ('author', models.ForeignKey(related_name='comments', to='Hindlebook.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=100, unique=True)),
                ('host_name', models.CharField(max_length=50, default='', blank=True)),
                ('share_posts', models.BooleanField(default=True)),
                ('share_images', models.BooleanField(default=True)),
                ('require_auth', models.BooleanField(default=True)),
                ('password', models.CharField(max_length=128, default='', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('guid', models.CharField(serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, default=uuid.uuid4, primary_key=True, blank=True)),
                ('source', models.CharField(max_length=100, default='Unknown source', blank=True)),
                ('origin', models.CharField(max_length=100, default='Unknown origin', blank=True)),
                ('title', models.CharField(max_length=40, default='No title', blank=True)),
                ('description', models.CharField(max_length=40, default='No description', blank=True)),
                ('content', models.TextField()),
                ('pubDate', models.DateTimeField(auto_now_add=True, verbose_name='date published', db_index=True)),
                ('content_type', models.CharField(max_length=15, choices=[('text/plain', 'text/plain'), ('text/x-markdown', 'text/x-markdown'), ('text/html', 'text/html')], default='text/html', blank=True)),
                ('visibility', models.CharField(max_length=10, choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], default='PUBLIC', db_index=True)),
                ('author', models.ForeignKey(related_name='posts', to='Hindlebook.Author')),
                ('categories', models.ManyToManyField(related_name='tagged_posts', to='Hindlebook.Category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('connection_limit', models.IntegerField(default=10, blank=True)),
                ('local_node', models.OneToOneField(to='Hindlebook.Node', null=True)),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='image',
            name='attached_to',
            field=models.ForeignKey(to='Hindlebook.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='Hindlebook.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='node',
            field=models.ForeignKey(related_name='authors', to='Hindlebook.Node'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='author', null=True, blank=True),
            preserve_default=True,
        ),
    ]
