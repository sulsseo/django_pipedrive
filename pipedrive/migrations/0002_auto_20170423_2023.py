# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dealfield',
            old_name='field_kind',
            new_name='field_type',
        ),
        migrations.RenameField(
            model_name='organizationfield',
            old_name='field_kind',
            new_name='field_type',
        ),
        migrations.RenameField(
            model_name='personfield',
            old_name='field_kind',
            new_name='field_type',
        ),
    ]
