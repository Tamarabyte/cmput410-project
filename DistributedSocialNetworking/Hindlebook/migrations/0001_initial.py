# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings
import Hindlebook.models.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('about', models.CharField(blank=True, default='', max_length=250)),
                ('uuid', models.CharField(primary_key=True, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, default=uuid.uuid4, serialize=False, blank=True)),
                ('username', models.CharField(verbose_name='username', max_length=30)),
                ('github_id', models.CharField(blank=True, default='', max_length=30)),
                ('avatar', models.ImageField(blank=True, default='default_avatar.jpg', upload_to='')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('follows', models.ManyToManyField(to='Hindlebook.Author', db_index=True, related_name='followed_by', blank=True)),
                ('friends', models.ManyToManyField(to='Hindlebook.Author', db_index=True, related_name='friends_of', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('tag', models.CharField(serialize=False, primary_key=True, max_length=25)),
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
                ('guid', models.CharField(primary_key=True, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, default=uuid.uuid4, serialize=False, blank=True)),
                ('comment', models.CharField(max_length=2048)),
                ('pubDate', models.DateTimeField(verbose_name='date published', db_index=True, auto_now_add=True)),
                ('author', models.ForeignKey(to='Hindlebook.Author', related_name='comments')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('host', models.CharField(max_length=100, unique=True)),
                ('host_name', models.CharField(blank=True, default='', max_length=50)),
                ('share_posts', models.BooleanField(default=True)),
                ('share_images', models.BooleanField(default=True)),
                ('require_auth', models.BooleanField(default=True)),
                ('password', models.CharField(blank=True, default='', max_length=128)),
                ('our_username', models.CharField(blank=True, default='', max_length=128)),
                ('our_password', models.CharField(blank=True, default='', max_length=128)),
                ('team_number', models.IntegerField(default=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('guid', models.CharField(primary_key=True, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, default=uuid.uuid4, serialize=False, blank=True)),
                ('source', models.CharField(blank=True, default='Unknown source', max_length=100)),
                ('origin', models.CharField(blank=True, default='Unknown origin', max_length=100)),
                ('title', models.CharField(blank=True, default='No title', max_length=40)),
                ('description', models.CharField(blank=True, default='No description', max_length=40)),
                ('content', models.TextField()),
                ('pubDate', models.DateTimeField(verbose_name='date published', db_index=True, auto_now_add=True)),
                ('content_type', models.CharField(choices=[('text/plain', 'text/plain'), ('text/x-markdown', 'text/x-markdown'), ('text/html', 'text/html')], blank=True, default='text/html', max_length=15)),
                ('visibility', models.CharField(db_index=True, choices=[('PUBLIC', 'Public'), ('FOAF', 'Friends of Friends Only'), ('FRIENDS', 'Friends Only'), ('PRIVATE', 'Private'), ('SERVERONLY', 'Server Only')], max_length=10, default='PUBLIC')),
                ('author', models.ForeignKey(to='Hindlebook.Author', related_name='posts')),
                ('categories', models.ManyToManyField(to='Hindlebook.Category', related_name='tagged_posts', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('connection_limit', models.IntegerField(blank=True, default=10)),
                ('node', models.ForeignKey(default=1, to='Hindlebook.Node', null=True)),
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
            field=models.ForeignKey(to='Hindlebook.Post', related_name='comments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='node',
            field=models.ForeignKey(to='Hindlebook.Node', related_name='authors'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(blank=True, related_name='author', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
