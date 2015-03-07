# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0001_initial'),
    ]

    operations = [
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
            field=models.CharField(default="This user hasn't filled out their profile yet!", blank=True, max_length=250),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(height_field=100, blank=True, width_field=100, null=True, upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='github_id',
            field=models.CharField(default='', blank=True, max_length=30),
            preserve_default=True,
        ),
    ]
