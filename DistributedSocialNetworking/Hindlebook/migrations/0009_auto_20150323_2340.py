# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0008_auto_20150323_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default='66e04970-e7ae-4c23-8116-d2656235e87f', to='Hindlebook.Author', related_name='comments'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default='66e04970-e7ae-4c23-8116-d2656235e87f', to='Hindlebook.Author', related_name='posts'),
            preserve_default=False,
        ),
    ]
