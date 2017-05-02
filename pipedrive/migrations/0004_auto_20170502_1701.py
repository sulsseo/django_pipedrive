# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pipedrive', '0003_fieldmodification'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='dealfield',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='dealfield',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organizationfield',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='organizationfield',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='personfield',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='personfield',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
