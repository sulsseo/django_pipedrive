# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0021_auto_20170420_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='creator_user_id',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='external_user_id',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='pipeline_id',
        ),
        migrations.AddField(
            model_name='deal',
            name='creator_user',
            field=models.ForeignKey(related_name='creator', to_field=b'external_id', blank=True, to='pipedrive.User', null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='user',
            field=models.ForeignKey(related_name='user', to_field=b'external_id', blank=True, to='pipedrive.User', null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='pipeline',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Pipeline', null=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='active_flag',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='stage',
            name='external_id',
            field=models.IntegerField(db_index=True, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='order_nr',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
