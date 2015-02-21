# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0004_auto_20150216_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='attached_to',
            field=models.ManyToManyField(to='Hindlebook.Post', null=True),
            preserve_default=True,
        ),
    ]
