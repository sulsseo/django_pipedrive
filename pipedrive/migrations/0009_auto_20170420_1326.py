# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0008_auto_20170420_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='external_organization_id',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Organization', null=True),
        ),
    ]
