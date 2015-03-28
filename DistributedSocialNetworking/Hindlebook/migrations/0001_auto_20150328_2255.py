# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', 'node_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pubDate',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True, verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='pubDate',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True, verbose_name='date published'),
            preserve_default=True,
        ),
    ]
