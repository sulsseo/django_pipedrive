# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('upload_timestamp', models.DateTimeField(null=True, blank=True)),
                ('external_deal_id', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('external_person_id', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('last_updated_at', models.DateTimeField(null=True, blank=True)),
                ('creator_user_id', models.IntegerField(null=True)),
                ('external_user_id', models.IntegerField(null=True)),
                ('value', models.IntegerField(null=True)),
                ('external_org_id', models.IntegerField(null=True)),
                ('external_pipeline_id', models.IntegerField(null=True)),
                ('external_stage_id', models.IntegerField(null=True)),
                ('add_time', models.DateTimeField(null=True, blank=True)),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('stage_change_time', models.DateTimeField(null=True, blank=True)),
                ('next_activity_datetime', models.DateTimeField(null=True, blank=True)),
                ('last_activity_datetime', models.DateTimeField(null=True, blank=True)),
                ('won_time', models.DateTimeField(null=True, blank=True)),
                ('last_incoming_mail_time', models.DateTimeField(null=True, blank=True)),
                ('last_outgoing_mail_time', models.DateTimeField(null=True, blank=True)),
                ('lost_time', models.DateTimeField(null=True, blank=True)),
                ('close_time', models.DateTimeField(null=True, blank=True)),
                ('lost_reason', models.CharField(max_length=255, null=True, blank=True)),
                ('visible_to', models.IntegerField(default=0, choices=[(0, b'private'), (3, b'shared')])),
                ('activities_count', models.IntegerField(null=True)),
                ('done_activities_count', models.IntegerField(null=True)),
                ('undone_activities_count', models.IntegerField(null=True)),
                ('email_messages_count', models.IntegerField(null=True)),
                ('expected_close_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DealField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(null=True)),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('field_kind', models.CharField(max_length=255)),
                ('active_flag', models.NullBooleanField()),
                ('mandatory_flag', models.NullBooleanField()),
                ('edit_flag', models.NullBooleanField()),
                ('is_subfield', models.NullBooleanField()),
                ('retrieved_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(null=True)),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('field_kind', models.CharField(max_length=255)),
                ('active_flag', models.NullBooleanField()),
                ('mandatory_flag', models.NullBooleanField()),
                ('edit_flag', models.NullBooleanField()),
                ('is_subfield', models.NullBooleanField()),
                ('retrieved_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField(null=True)),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('field_kind', models.CharField(max_length=255)),
                ('active_flag', models.NullBooleanField()),
                ('mandatory_flag', models.NullBooleanField()),
                ('edit_flag', models.NullBooleanField()),
                ('is_subfield', models.NullBooleanField()),
                ('retrieved_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('active_flag', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField()),
                ('pipeline_id', models.IntegerField()),
                ('pipeline_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('order_nr', models.IntegerField()),
                ('active_flag', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='organization',
            name='pipedrive_id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='person',
            name='pipedrive_id',
        ),
        migrations.AddField(
            model_name='organization',
            name='activities_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='add_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='address',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='closed_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='done_activities_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='email_messages_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='external_organization_id',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_activity_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_updated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='lost_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='next_activity_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='open_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='undone_activities_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='visible_to',
            field=models.IntegerField(default=0, choices=[(0, b'private'), (3, b'shared')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='won_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='activities_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='add_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='closed_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='done_activities_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='email_messages_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='external_person_id',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_activity_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_incoming_mail_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_outgoing_mail_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='last_updated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='lost_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='next_activity_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='open_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='org_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='owner_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='undone_activities_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='visible_to',
            field=models.IntegerField(default=0, choices=[(0, b'private'), (3, b'shared')]),
        ),
        migrations.AddField(
            model_name='person',
            name='won_deals_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='update_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='update_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='buyer_organization',
            field=models.ForeignKey(related_name='buyer_organizations', blank=True, to='pipedrive.Organization', null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='person',
            field=models.ForeignKey(blank=True, to='pipedrive.Person', null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='provider_organization',
            field=models.ForeignKey(related_name='provider_organizations', blank=True, to='pipedrive.Organization', null=True),
        ),
    ]
