# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0007_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='tag',
            field=models.CharField(unique=True, max_length=25),
            preserve_default=True,
        ),
    ]
