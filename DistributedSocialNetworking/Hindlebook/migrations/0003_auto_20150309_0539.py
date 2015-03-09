# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0002_auto_20150309_0412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Tags', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'verbose_name_plural': 'Server'},
        ),
    ]
