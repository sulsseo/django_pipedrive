# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0003_auto_20170419_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('external_user_id', models.IntegerField(null=True, blank=True)),
                ('external_deal_id', models.IntegerField(null=True, blank=True)),
                ('external_person_id', models.IntegerField(null=True, blank=True)),
                ('external_org_id', models.IntegerField(null=True, blank=True)),
                ('content', models.CharField(max_length=1024, null=True, blank=True)),
                ('add_time', models.DateTimeField(null=True, blank=True)),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('active_flag', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
