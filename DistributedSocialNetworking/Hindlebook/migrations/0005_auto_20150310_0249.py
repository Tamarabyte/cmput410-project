# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Hindlebook.models.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0004_auto_20150309_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='post',
            name='uuid',
        ),
        migrations.AddField(
            model_name='comment',
            name='guid',
            field=models.CharField(max_length=40, default=uuid.uuid4, serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], primary_key=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='guid',
            field=models.CharField(max_length=40, default=uuid.uuid4, serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], primary_key=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='foreignuser',
            name='uuid',
            field=models.CharField(max_length=40, default=uuid.uuid4, serialize=False, validators=[Hindlebook.models.validators.UuidValidator()], primary_key=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(db_index=True, max_length=40, validators=[Hindlebook.models.validators.UuidValidator()], default=uuid.uuid4, blank=True),
            preserve_default=True,
        ),
    ]
