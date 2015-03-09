# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='server',
            new_name='node',
        ),
        migrations.RemoveField(
            model_name='user',
            name='host',
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.IntegerField(choices=[(0, 'text/plain'), (1, 'text/x-markdown'), (2, 'text/html')], default=0, max_length=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.IntegerField(choices=[(0, 'PUBLIC'), (1, 'FOAF'), (2, 'FRIENDS'), (3, 'PRIVATE'), (4, 'SERVERONLY')], default=0, max_length=1, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(db_index=True, related_name='followed_by', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='follows_foreign',
            field=models.ManyToManyField(db_index=True, related_name='follows_foreign_rel_+', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(db_index=True, default=uuid.uuid4, max_length=40, blank=True),
            preserve_default=True,
        ),
    ]
