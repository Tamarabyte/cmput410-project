# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0007_auto_20150323_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(db_index=True, related_name='friends_of', to='Hindlebook.Author', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='author'),
            preserve_default=True,
        ),
    ]
