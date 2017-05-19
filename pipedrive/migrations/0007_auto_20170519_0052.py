# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pipedrive.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0006_auto_20170512_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='note',
            field=pipedrive.fields.TruncatingCharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='subject',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='lost_reason',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='title',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dealfield',
            name='field_type',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='dealfield',
            name='key',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='dealfield',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='fieldmodification',
            name='current_value',
            field=pipedrive.fields.TruncatingCharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='fieldmodification',
            name='field_name',
            field=pipedrive.fields.TruncatingCharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='fieldmodification',
            name='previous_value',
            field=pipedrive.fields.TruncatingCharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='content',
            field=pipedrive.fields.TruncatingCharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organizationfield',
            name='field_type',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='organizationfield',
            name='key',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='organizationfield',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='personfield',
            name='field_type',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='personfield',
            name='key',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='personfield',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='url_title',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='stage',
            name='pipeline_name',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=pipedrive.fields.TruncatingCharField(max_length=500, null=True, blank=True),
        ),
    ]
