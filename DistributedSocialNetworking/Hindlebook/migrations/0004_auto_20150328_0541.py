# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0003_auto_20150326_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='is_connected',
            field=models.BooleanField(default=False, help_text='Whether or not we actively pull posts/authors from this node.', verbose_name='connect_with'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.OneToOneField(help_text='Set for local authors only', related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='host',
            field=models.CharField(help_text='URL of the host. ex. http://hindlebook.tamarabyte.com ', max_length=100, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='host_name',
            field=models.CharField(max_length=50, help_text='Username/short identifier of host. ex. hindlebook', verbose_name='username', default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='our_password',
            field=models.CharField(max_length=128, help_text='Password this node wants from us.', verbose_name='password', default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='our_username',
            field=models.CharField(max_length=128, help_text='Username this node wants from us.', verbose_name='username', default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='password',
            field=models.CharField(default='', help_text='Password this node connects to us with.', max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
