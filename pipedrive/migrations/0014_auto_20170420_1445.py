# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0013_auto_20170420_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='external_user_id',
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.User', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='external_id',
            field=models.IntegerField(db_index=True, unique=True, null=True, blank=True),
        ),
    ]
