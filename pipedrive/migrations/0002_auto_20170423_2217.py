# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='dealfield',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='organizationfield',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='personfield',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='additional_fields',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True),
        ),
    ]
