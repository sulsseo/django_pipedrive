# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0014_auto_20170420_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('done', models.NullBooleanField()),
                ('subject', models.CharField(max_length=255, null=True, blank=True)),
                ('note', models.CharField(max_length=1024, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('due_time', models.TimeField(null=True, blank=True)),
                ('duration', models.TimeField(null=True, blank=True)),
                ('marked_as_done_time', models.TimeField(null=True, blank=True)),
                ('active_flag', models.NullBooleanField()),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('add_time', models.DateTimeField(null=True, blank=True)),
                ('deal', models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Deal', null=True)),
                ('org', models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Organization', null=True)),
                ('person', models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.Person', null=True)),
                ('user', models.ForeignKey(to_field=b'external_id', blank=True, to='pipedrive.User', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
