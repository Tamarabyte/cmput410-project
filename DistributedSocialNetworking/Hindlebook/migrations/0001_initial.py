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
                ('about', models.CharField(default='', max_length=250, blank=True)),
                ('uuid', models.CharField(validators=[Hindlebook.models.validators.UuidValidator()], primary_key=True, default=uuid.uuid4, max_length=40, serialize=False, blank=True)),
                ('username', models.CharField(verbose_name='username', max_length=30)),
                ('github_id', models.CharField(default='', max_length=30, blank=True)),
                ('avatar', models.ImageField(default='default_avatar.jpg', upload_to='', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('follows', models.ManyToManyField(db_index=True, related_name='followed_by', blank=True, to='Hindlebook.Author')),
                ('friends', models.ManyToManyField(db_index=True, related_name='friends_of', blank=True, to='Hindlebook.Author')),
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
                ('guid', models.CharField(validators=[Hindlebook.models.validators.UuidValidator()], primary_key=True, default=uuid.uuid4, max_length=40, serialize=False, blank=True)),
                ('comment', models.CharField(max_length=2048)),
                ('pubDate', models.DateTimeField(verbose_name='date published', db_index=True, auto_now_add=True)),
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
                ('host', models.CharField(max_length=100, unique=True, serialize=False, primary_key=True)),
                ('host_name', models.CharField(default='', max_length=50, blank=True)),
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
                ('guid', models.CharField(validators=[Hindlebook.models.validators.UuidValidator()], primary_key=True, default=uuid.uuid4, max_length=40, serialize=False, blank=True)),
                ('source', models.CharField(default='Unknown source', max_length=100, blank=True)),
                ('origin', models.CharField(default='Unknown origin', max_length=100, blank=True)),
                ('title', models.CharField(default='No title', max_length=40, blank=True)),
                ('description', models.CharField(default='No description', max_length=40, blank=True)),
                ('content', models.TextField()),
                ('pubDate', models.DateTimeField(verbose_name='date published', db_index=True, auto_now_add=True)),
                ('content_type', models.CharField(default='text/html', max_length=15, choices=[('text/plain', 'text/plain'), ('text/x-markdown', 'text/x-markdown'), ('text/html', 'text/html')], blank=True)),
                ('visibility', models.CharField(default='PUBLIC', max_length=10, choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], db_index=True)),
                ('author', models.ForeignKey(related_name='posts', to='Hindlebook.Author')),
                ('categories', models.ManyToManyField(related_name='tagged_posts', blank=True, to='Hindlebook.Category')),
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
            field=models.OneToOneField(null=True, related_name='author', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
