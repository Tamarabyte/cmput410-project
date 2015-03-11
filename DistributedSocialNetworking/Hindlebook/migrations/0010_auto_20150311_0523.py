# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0009_auto_20150311_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='tag',
            field=models.CharField(unique=True, max_length=25),
            preserve_default=True,
        ),
    ]
