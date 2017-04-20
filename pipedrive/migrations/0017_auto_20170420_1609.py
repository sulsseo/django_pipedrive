# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0016_auto_20170420_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipeline',
            name='active_flag',
        ),
        migrations.AddField(
            model_name='pipeline',
            name='active',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='add_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='update_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='url_title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='external_id',
            field=models.IntegerField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
