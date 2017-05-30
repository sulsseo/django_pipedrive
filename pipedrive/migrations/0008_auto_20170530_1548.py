# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pipedrive.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0007_auto_20170519_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='stage',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Stage', null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='status',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
    ]
