# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0002_auto_20150216_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follow',
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, to='Hindlebook.User', related_name='followed_by'),
            preserve_default=True,
        ),
    ]
