# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0003_auto_20150308_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=40),
            preserve_default=True,
        ),
    ]
