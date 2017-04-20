# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0019_auto_20170420_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='owner_id',
        ),
        migrations.AddField(
            model_name='person',
            name='owner',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.User', null=True),
        ),
    ]
