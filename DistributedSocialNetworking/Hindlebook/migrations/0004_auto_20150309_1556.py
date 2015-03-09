# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0003_auto_20150309_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='', blank=True, default='default_avatar.jpg'),
            preserve_default=True,
        ),
    ]
