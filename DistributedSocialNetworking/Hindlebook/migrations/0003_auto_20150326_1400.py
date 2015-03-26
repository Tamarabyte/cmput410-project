# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0002_auto_20150326_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(default='text/plain', choices=[('text/plain', 'Text'), ('text/x-markdown', 'Markdown'), ('text/html', 'HTML')], blank=True, max_length=15),
            preserve_default=True,
        ),
    ]
