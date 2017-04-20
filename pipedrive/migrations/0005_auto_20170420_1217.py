# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0004_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='external_id',
            field=models.CharField(db_index=True, max_length=255, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='external_person_id',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Person', null=True),
        ),
    ]
