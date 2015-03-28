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
                ('about', models.CharField(default='', blank=True, max_length=250)),
                ('uuid', models.CharField(default=uuid.uuid4, blank=True, serialize=False, primary_key=True, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40)),
                ('username', models.CharField(max_length=30, verbose_name='username')),
                ('github_id', models.CharField(default='', blank=True, max_length=30)),
                ('avatar', models.ImageField(upload_to='', default='default_avatar.jpg', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('follows', models.ManyToManyField(blank=True, db_index=True, to='Hindlebook.Author', related_name='followed_by')),
                ('friends', models.ManyToManyField(blank=True, db_index=True, to='Hindlebook.Author', related_name='friends_of')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('tag', models.CharField(max_length=15, serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'ordering': ['tag'],
                'verbose_name': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('guid', models.CharField(default=uuid.uuid4, blank=True, serialize=False, primary_key=True, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40)),
                ('comment', models.CharField(max_length=2048)),
                ('pubDate', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date published')),
                ('author', models.ForeignKey(related_name='comments', to='Hindlebook.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('host', models.CharField(unique=True, max_length=100, help_text='URL of the host. ex. http://hindlebook.tamarabyte.com ')),
                ('host_name', models.CharField(default='', blank=True, max_length=50, help_text='Username/short identifier of host. ex. hindlebook', verbose_name='username')),
                ('is_connected', models.BooleanField(default=False, help_text='Whether or not we actively pull posts/authors from this node.', verbose_name='connect_with')),
                ('share_posts', models.BooleanField(default=True)),
                ('share_images', models.BooleanField(default=True)),
                ('require_auth', models.BooleanField(default=True)),
                ('password', models.CharField(default='', blank=True, max_length=128, help_text='Password this node connects to us with.')),
                ('our_username', models.CharField(default='', blank=True, max_length=128, help_text='Username this node wants from us.', verbose_name='username')),
                ('our_password', models.CharField(default='', blank=True, max_length=128, help_text='Password this node wants from us.', verbose_name='password')),
                ('team_number', models.IntegerField(default=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('guid', models.CharField(default=uuid.uuid4, blank=True, serialize=False, primary_key=True, validators=[Hindlebook.models.validators.UuidValidator()], max_length=40)),
                ('source', models.CharField(default='', blank=True, max_length=100)),
                ('origin', models.CharField(default='', blank=True, max_length=100)),
                ('title', models.CharField(default='', max_length=40)),
                ('description', models.CharField(default='', blank=True, max_length=40)),
                ('content', models.TextField()),
                ('pubDate', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date published')),
                ('content_type', models.CharField(choices=[('text/plain', 'Text'), ('text/x-markdown', 'Markdown'), ('text/html', 'HTML')], default='text/plain', blank=True, max_length=15)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FOAF', 'Friends of Friends Only'), ('FRIENDS', 'Friends Only'), ('PRIVATE', 'Private'), ('SERVERONLY', 'Server Only')], default='PUBLIC', max_length=10, db_index=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('connection_limit', models.IntegerField(default=10, blank=True)),
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
            field=models.OneToOneField(related_name='author', blank=True, help_text='Set for local authors only', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
