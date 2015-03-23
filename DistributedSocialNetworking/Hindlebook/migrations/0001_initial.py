# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import Hindlebook.models.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('about', models.CharField(max_length=250, blank=True, default='')),
                ('uuid', models.CharField(serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], blank=True, primary_key=True, max_length=40, default=uuid.uuid4)),
                ('username', models.CharField(verbose_name='username', max_length=30)),
                ('github_id', models.CharField(max_length=30, blank=True, default='')),
                ('avatar', models.ImageField(blank=True, default='default_avatar.jpg', upload_to='')),
                ('is_foreign', models.BooleanField(default=False)),
                ('follows', models.ManyToManyField(to='Hindlebook.Author', blank=True, db_index=True, related_name='followed_by')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('tag', models.CharField(serialize=False, max_length=25, primary_key=True)),
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
                ('guid', models.CharField(serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], blank=True, primary_key=True, max_length=40, default=uuid.uuid4)),
                ('comment', models.CharField(max_length=2048)),
                ('pubDate', models.DateTimeField(verbose_name='date published', auto_now_add=True, db_index=True)),
                ('author', models.ForeignKey(blank=True, related_name='comments', to='Hindlebook.Author', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('host', models.CharField(serialize=False, max_length=100, unique=True, primary_key=True)),
                ('host_name', models.CharField(max_length=50, blank=True, default='')),
                ('share_posts', models.BooleanField(default=True)),
                ('share_images', models.BooleanField(default=True)),
                ('require_auth', models.BooleanField(default=True)),
                ('password', models.CharField(max_length=128, blank=True, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('guid', models.CharField(serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], blank=True, primary_key=True, max_length=40, default=uuid.uuid4)),
                ('source', models.CharField(max_length=100, blank=True, default='Unknown source')),
                ('origin', models.CharField(max_length=100, blank=True, default='Unknown origin')),
                ('title', models.CharField(max_length=40, blank=True, default='No title')),
                ('description', models.CharField(max_length=40, blank=True, default='No description')),
                ('content', models.TextField()),
                ('pubDate', models.DateTimeField(verbose_name='date published', auto_now_add=True, db_index=True)),
                ('content_type', models.CharField(max_length=15, choices=[('text/plain', 'text/plain'), ('text/x-markdown', 'text/x-markdown'), ('text/html', 'text/html')], blank=True, default='text/html')),
                ('visibility', models.CharField(max_length=10, choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], default='PUBLIC', db_index=True)),
                ('author', models.ForeignKey(blank=True, related_name='posts', to='Hindlebook.Author', null=True)),
                ('categories', models.ManyToManyField(to='Hindlebook.Category', blank=True, related_name='tagged_posts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('connection_limit', models.IntegerField(blank=True, default=10)),
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
            field=models.ForeignKey(to='Hindlebook.Node', related_name='users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
