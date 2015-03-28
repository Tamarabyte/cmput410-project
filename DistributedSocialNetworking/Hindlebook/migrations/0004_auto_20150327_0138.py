# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0003_auto_20150326_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True, help_text='Set for local authors only'),
            preserve_default=True,
        ),
    ]
