# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0022_auto_20170420_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='pipeline_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
