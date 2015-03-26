# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', 'node_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Tags', 'ordering': ['tag'], 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterField(
            model_name='category',
            name='tag',
            field=models.CharField(max_length=15, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=40, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.CharField(max_length=100, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.CharField(max_length=100, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=40, default='', blank=True),
            preserve_default=True,
        ),
    ]
