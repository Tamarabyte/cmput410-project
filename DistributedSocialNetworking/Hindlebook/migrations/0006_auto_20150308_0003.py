# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0005_auto_20150307_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.IntegerField(choices=[(0, 'Self Only'), (1, 'Selected author'), (2, 'Friends'), (3, 'Friends of Friends'), (4, 'Friends on host'), (5, 'Public')], max_length=1, default=5),
            preserve_default=True,
        ),
    ]
