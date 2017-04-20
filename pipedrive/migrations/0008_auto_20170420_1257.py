# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0007_auto_20170420_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='organization',
            new_name='org',
        ),
    ]
