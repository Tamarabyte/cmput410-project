# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0014_auto_20150313_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='friends_of', db_index=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='friends_foreign',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='friends_foreign_rel_+', db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
