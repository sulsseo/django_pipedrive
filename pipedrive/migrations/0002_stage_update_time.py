# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='update_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
