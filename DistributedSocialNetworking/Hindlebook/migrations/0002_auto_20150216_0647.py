# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='follow_rel_+', to='Hindlebook.User'),
            preserve_default=True,
        ),
    ]
