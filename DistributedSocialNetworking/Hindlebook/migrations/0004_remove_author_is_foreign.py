# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0003_author_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='is_foreign',
        ),
    ]
