# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0011_auto_20170420_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='external_org_id',
        ),
        migrations.AddField(
            model_name='deal',
            name='org',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Organization', null=True),
        ),
    ]
