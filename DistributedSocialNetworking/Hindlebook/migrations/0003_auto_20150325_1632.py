# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='our_password',
            field=models.CharField(blank=True, default='', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='our_username',
            field=models.CharField(blank=True, default='', max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(default='PUBLIC', choices=[('PUBLIC', 'Public'), ('FOAF', 'Friends of Friends Only'), ('FRIENDS', 'Friends Only'), ('PRIVATE', 'Private'), ('SERVERONLY', 'Server Only')], db_index=True, max_length=10),
            preserve_default=True,
        ),
    ]
