# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0006_auto_20170420_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='external_deal_id',
        ),
        migrations.RemoveField(
            model_name='note',
            name='external_org_id',
        ),
        migrations.AddField(
            model_name='note',
            name='deal',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Deal', null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='organization',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='external_id',
            field=models.CharField(db_index=True, max_length=255, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='external_id',
            field=models.CharField(db_index=True, max_length=255, unique=True, null=True, blank=True),
        ),
    ]
