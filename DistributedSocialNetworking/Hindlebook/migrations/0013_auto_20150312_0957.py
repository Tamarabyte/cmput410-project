# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0012_auto_20150311_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
        migrations.AlterField(
            model_name='category',
            name='tag',
            field=models.CharField(max_length=25, primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
