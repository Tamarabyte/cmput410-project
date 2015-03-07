# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0004_post_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.IntegerField(default=5, max_length=1, choices=[(0, b'Self Only'), (1, b'Selected author'), (2, b'Friends'), (3, b'Friends of Friends'), (4, b'Friends on host'), (5, b'Public')]),
            preserve_default=True,
        ),
    ]
