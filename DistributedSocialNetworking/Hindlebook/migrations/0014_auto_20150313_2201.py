# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0013_auto_20150312_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='host_name',
            field=models.CharField(max_length=50, default='', blank=True),
            preserve_default=True,
        ),
    ]
