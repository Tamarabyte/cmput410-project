# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Hindlebook.models.validators
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('Hindlebook', '0010_auto_20150311_0523'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='foreign_author',
        ),
        migrations.RemoveField(
            model_name='node',
            name='id',
        ),
        migrations.AddField(
            model_name='comment',
            name='genericAuthor',
            field=models.ForeignKey(null=True, blank=True, to='Hindlebook.GenericUser', related_name='comments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foreignuser',
            name='id',
            field=models.AutoField(default=1, verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='genericAuthor',
            field=models.ForeignKey(null=True, blank=True, to='Hindlebook.GenericUser', related_name='posts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='foreignuser',
            name='uuid',
            field=models.CharField(validators=[Hindlebook.models.validators.UuidValidator()], max_length=40, blank=True, default=uuid.uuid4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='node',
            name='host',
            field=models.CharField(serialize=False, max_length=100, primary_key=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='posts'),
            preserve_default=True,
        ),
    ]
