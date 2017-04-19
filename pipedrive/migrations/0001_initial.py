# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pipedrive_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=255)),
                ('owner_id', models.IntegerField(null=True)),
                ('people_count', models.IntegerField(null=True)),
                ('update_time', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pipedrive_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('update_time', models.DateTimeField(verbose_name=b'date published')),
                ('organization', models.ForeignKey(to='pipedrive.Organization')),
            ],
        ),
    ]
