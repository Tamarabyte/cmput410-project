# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0003_auto_20150307_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.IntegerField(default=5),
            preserve_default=True,
        ),
    ]
