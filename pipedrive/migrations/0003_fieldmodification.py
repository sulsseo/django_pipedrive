# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pipedrive', '0002_auto_20170423_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_name', models.CharField(max_length=1024, null=True, blank=True)),
                ('previous_value', models.CharField(max_length=1024, null=True, blank=True)),
                ('current_value', models.CharField(max_length=1024, null=True, blank=True)),
                ('created', models.DateTimeField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
