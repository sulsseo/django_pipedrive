# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0004_auto_20170502_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='subject',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='lost_reason',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='title',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dealfield',
            name='field_type',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='dealfield',
            name='key',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='dealfield',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organizationfield',
            name='field_type',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='organizationfield',
            name='key',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='organizationfield',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='personfield',
            name='field_type',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='personfield',
            name='key',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='personfield',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='name',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='url_title',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='stage',
            name='pipeline_name',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
