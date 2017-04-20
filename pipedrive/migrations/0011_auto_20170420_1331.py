# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0010_auto_20170420_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='external_person_id',
        ),
        migrations.AlterField(
            model_name='deal',
            name='person',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Person', null=True),
        ),
    ]
