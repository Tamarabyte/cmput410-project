# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0004_remove_author_is_foreign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='node',
            field=models.ForeignKey(related_name='authors', to='Hindlebook.Node'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(blank=True, null=True, related_name='author_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
