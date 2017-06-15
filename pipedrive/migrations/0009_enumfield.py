# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pipedrive.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pipedrive', '0008_auto_20170530_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnumField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('label', pipedrive.fields.TruncatingCharField(max_length=500)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
