# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=2048)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pub_date', models.DateTimeField(verbose_name='date published', auto_now_add=True)),
                ('privacy_level', models.IntegerField()),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_image', models.ImageField(blank=True, upload_to='', null=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(primary_key=True, max_length=75, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('github_id', models.CharField(null=True, max_length=30)),
                ('join_date', models.DateField(verbose_name='date joined', auto_now_add=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='followers_rel_+', to='Hindlebook.User')),
                ('following', models.ManyToManyField(blank=True, related_name='following_rel_+', to='Hindlebook.User')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_rel_+', to='Hindlebook.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to='Hindlebook.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='Hindlebook.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='attached_to',
            field=models.ManyToManyField(to='Hindlebook.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='Hindlebook.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='Hindlebook.Post'),
            preserve_default=True,
        ),
    ]
