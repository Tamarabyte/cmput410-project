# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0002_load_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 3, 23, 21, 31, 36, 237745, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
