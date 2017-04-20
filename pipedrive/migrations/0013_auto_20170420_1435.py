# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0012_auto_20170420_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.CharField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('last_login', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('role_id', models.IntegerField(null=True, blank=True)),
                ('active_flag', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='deal',
            name='expected_close_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
