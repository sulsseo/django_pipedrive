# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0008_auto_20170530_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='order_nr',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
