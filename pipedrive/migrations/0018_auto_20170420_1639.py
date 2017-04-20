# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0017_auto_20170420_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='external_pipeline_id',
        ),
        migrations.RemoveField(
            model_name='pipeline',
            name='external_id',
        ),
    ]
