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
                ('about', models.CharField(default='', blank=True, max_length=250)),
                ('uuid', models.CharField(blank=True, primary_key=True, serialize=False, default=uuid.uuid4, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40)),
                ('username', models.CharField(max_length=30, verbose_name='username')),
                ('github_id', models.CharField(default='', blank=True, max_length=30)),
                ('avatar', models.ImageField(default='default_avatar.jpg', blank=True, upload_to='')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('follows', models.ManyToManyField(blank=True, to='Hindlebook.Author', related_name='followed_by', db_index=True)),
                ('friends', models.ManyToManyField(blank=True, to='Hindlebook.Author', related_name='friends_of', db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('tag', models.CharField(primary_key=True, max_length=25, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('guid', models.CharField(blank=True, primary_key=True, serialize=False, default=uuid.uuid4, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40)),
                ('comment', models.CharField(max_length=2048)),
                ('pubDate', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='date published')),
                ('author', models.ForeignKey(related_name='comments', to='Hindlebook.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('host', models.CharField(max_length=100, unique=True)),
                ('host_name', models.CharField(default='', blank=True, max_length=50)),
                ('share_posts', models.BooleanField(default=True)),
                ('share_images', models.BooleanField(default=True)),
                ('require_auth', models.BooleanField(default=True)),
                ('password', models.CharField(default='', blank=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('guid', models.CharField(blank=True, primary_key=True, serialize=False, default=uuid.uuid4, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40)),
                ('source', models.CharField(default='Unknown source', blank=True, max_length=100)),
                ('origin', models.CharField(default='Unknown origin', blank=True, max_length=100)),
                ('title', models.CharField(default='No title', blank=True, max_length=40)),
                ('description', models.CharField(default='No description', blank=True, max_length=40)),
                ('content', models.TextField()),
                ('pubDate', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='date published')),
                ('content_type', models.CharField(default='text/html', blank=True, choices=[('text/plain', 'text/plain'), ('text/x-markdown', 'text/x-markdown'), ('text/html', 'text/html')], max_length=15)),
                ('visibility', models.CharField(default='PUBLIC', db_index=True, choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], max_length=10)),
                ('author', models.ForeignKey(related_name='posts', to='Hindlebook.Author')),
                ('categories', models.ManyToManyField(blank=True, to='Hindlebook.Category', related_name='tagged_posts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('connection_limit', models.IntegerField(default=10, blank=True)),
                ('node', models.ForeignKey(null=True, default=1, to='Hindlebook.Node')),
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
            field=models.OneToOneField(related_name='author', null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
