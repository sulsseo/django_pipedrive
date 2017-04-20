# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0018_auto_20170420_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='external_id',
            field=models.IntegerField(db_index=True, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='pipeline',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Pipeline', null=True),
        ),
    ]
