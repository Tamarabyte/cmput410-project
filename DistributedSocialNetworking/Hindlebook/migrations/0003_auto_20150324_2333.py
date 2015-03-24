# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0002_server_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='id',
            field=models.AutoField(default=1, serialize=False, auto_created=True, verbose_name='ID', primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settings',
            name='local_node',
            field=models.OneToOneField(to='Hindlebook.Node', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='host',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
