# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0005_auto_20170420_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='external_person_id',
            new_name='person',
        ),
    ]
