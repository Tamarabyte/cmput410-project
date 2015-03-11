# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0011_auto_20150311_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericuser',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='genericAuthor',
        ),
        migrations.RemoveField(
            model_name='post',
            name='genericAuthor',
        ),
        migrations.DeleteModel(
            name='GenericUser',
        ),
        migrations.AddField(
            model_name='comment',
            name='foreign_author',
            field=models.ForeignKey(blank=True, null=True, to='Hindlebook.ForeignUser', related_name='comments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='foreign_author',
            field=models.ForeignKey(blank=True, null=True, to='Hindlebook.ForeignUser', related_name='posts'),
            preserve_default=True,
        ),
    ]
