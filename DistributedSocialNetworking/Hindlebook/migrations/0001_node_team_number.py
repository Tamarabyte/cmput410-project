# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', 'node_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='team_number',
            field=models.IntegerField(default=9),
            preserve_default=True,
        ),
    ]
