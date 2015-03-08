# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_type',
            field=models.CharField(default='text/plain', max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default='No description', max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='origin',
            field=models.CharField(default='Unknown origin', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.IntegerField(default=5, max_length=1, choices=[(0, 'Self Only'), (1, 'Selected author'), (2, 'Friends'), (3, 'Friends of Friends'), (4, 'Friends on host'), (5, 'Public')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.CharField(default='Unknown source', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='No title', max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, unique=True, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='host',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, unique=True, max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='Hindlebook.Post'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.CharField(default="This user hasn't filled out their profile yet!", max_length=250, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(height_field=100, width_field=100, null=True, upload_to='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='github_id',
            field=models.CharField(default='', max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
