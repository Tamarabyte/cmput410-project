# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings
import Hindlebook.models.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0010_auto_20150311_0523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='id',
        ),
        migrations.AddField(
            model_name='foreignuser',
            name='id',
            field=models.AutoField(default=1, auto_created=True, serialize=False, primary_key=True, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='foreign_author',
            field=models.ForeignKey(to='Hindlebook.ForeignUser', null=True, related_name='posts', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='foreignuser',
            name='uuid',
            field=models.CharField(max_length=40, unique=True, validators=[Hindlebook.models.validators.UuidValidator()], default=uuid.uuid4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='host',
            field=models.CharField(max_length=100, unique=True, primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='posts', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, unique=True, db_index=True, max_length=40, validators=[Hindlebook.models.validators.UuidValidator()], blank=True),
            preserve_default=True,
        ),
    ]
