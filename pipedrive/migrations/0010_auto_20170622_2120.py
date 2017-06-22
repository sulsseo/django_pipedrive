# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0009_enumfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='external_id',
            field=models.IntegerField(db_index=True, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='external_id',
            field=models.IntegerField(db_index=True, unique=True, null=True, blank=True),
        ),
    ]
