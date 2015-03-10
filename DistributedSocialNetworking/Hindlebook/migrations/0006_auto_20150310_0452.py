# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0005_auto_20150310_0249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='pub_date',
            new_name='pubDate',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='pub_date',
            new_name='pubDate',
        ),
        migrations.RemoveField(
            model_name='post',
            name='privacy',
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(default='PUBLIC', db_index=True, choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(default='text/html', blank=True, choices=[('text/plain', 'text/plain'), ('text/x-markdown', 'text/x-markdown'), ('text/html', 'text/html')], max_length=15),
            preserve_default=True,
        ),
    ]
