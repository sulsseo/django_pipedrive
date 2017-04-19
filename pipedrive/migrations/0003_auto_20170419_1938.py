# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0002_auto_20170419_1914'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='org_id',
            new_name='external_organization_id',
        ),
    ]
