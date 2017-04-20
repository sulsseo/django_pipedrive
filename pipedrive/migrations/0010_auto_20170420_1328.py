# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0009_auto_20170420_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='external_organization_id',
            new_name='org',
        ),
    ]
