# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.postgres.operations import HStoreExtension
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(db_index=True, null=True, blank=True),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("done", models.NullBooleanField()),
                ("subject", models.CharField(max_length=255, null=True, blank=True)),
                ("note", models.CharField(max_length=1024, null=True, blank=True)),
                ("type", models.CharField(max_length=255, null=True, blank=True)),
                ("due_date", models.DateField(null=True, blank=True)),
                ("due_time", models.TimeField(null=True, blank=True)),
                ("duration", models.TimeField(null=True, blank=True)),
                ("marked_as_done_time", models.DateTimeField(null=True, blank=True)),
                ("active_flag", models.NullBooleanField()),
                ("update_time", models.DateTimeField(null=True, blank=True)),
                ("add_time", models.DateTimeField(null=True, blank=True)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Deal",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=255, null=True, blank=True)),
                ("upload_timestamp", models.DateTimeField(null=True, blank=True)),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("last_updated_at", models.DateTimeField(null=True, blank=True)),
                ("value", models.IntegerField(null=True)),
                ("external_stage_id", models.IntegerField(null=True)),
                ("add_time", models.DateTimeField(null=True, blank=True)),
                ("update_time", models.DateTimeField(null=True, blank=True)),
                ("stage_change_time", models.DateTimeField(null=True, blank=True)),
                ("next_activity_date", models.DateField(null=True, blank=True)),
                ("next_activity_time", models.TimeField(null=True, blank=True)),
                ("last_activity_date", models.DateField(null=True, blank=True)),
                ("last_activity_time", models.TimeField(null=True, blank=True)),
                ("won_time", models.DateTimeField(null=True, blank=True)),
                (
                    "last_incoming_mail_time",
                    models.DateTimeField(null=True, blank=True),
                ),
                (
                    "last_outgoing_mail_time",
                    models.DateTimeField(null=True, blank=True),
                ),
                ("lost_time", models.DateTimeField(null=True, blank=True)),
                ("close_time", models.DateTimeField(null=True, blank=True)),
                (
                    "lost_reason",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "visible_to",
                    models.IntegerField(
                        default=0, choices=[(0, b"private"), (3, b"shared")]
                    ),
                ),
                ("activities_count", models.IntegerField(null=True)),
                ("done_activities_count", models.IntegerField(null=True)),
                ("undone_activities_count", models.IntegerField(null=True)),
                ("email_messages_count", models.IntegerField(null=True)),
                ("expected_close_date", models.DateField(null=True, blank=True)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="DealField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("key", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("field_type", models.CharField(max_length=255)),
                ("active_flag", models.NullBooleanField()),
                ("mandatory_flag", models.NullBooleanField()),
                ("edit_flag", models.NullBooleanField()),
                ("is_subfield", models.NullBooleanField()),
                (
                    "retrieved_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(db_index=True, null=True, blank=True),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("content", models.CharField(max_length=1024, null=True, blank=True)),
                ("add_time", models.DateTimeField(null=True, blank=True)),
                ("update_time", models.DateTimeField(null=True, blank=True)),
                ("active_flag", models.NullBooleanField()),
                (
                    "deal",
                    models.ForeignKey(
                        to_field=b"external_id",
                        blank=True,
                        to="pipedrive.Deal",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("last_updated_at", models.DateTimeField(null=True, blank=True)),
                ("name", models.CharField(max_length=255, null=True, blank=True)),
                ("people_count", models.IntegerField(null=True)),
                ("open_deals_count", models.IntegerField(null=True)),
                ("add_time", models.DateTimeField(null=True, blank=True)),
                ("update_time", models.DateTimeField(null=True, blank=True)),
                (
                    "visible_to",
                    models.IntegerField(
                        default=0, choices=[(0, b"private"), (3, b"shared")]
                    ),
                ),
                ("next_activity_date", models.DateField(null=True, blank=True)),
                ("next_activity_time", models.TimeField(null=True, blank=True)),
                ("last_activity_date", models.DateField(null=True, blank=True)),
                ("last_activity_time", models.TimeField(null=True, blank=True)),
                ("won_deals_count", models.IntegerField(null=True)),
                ("lost_deals_count", models.IntegerField(null=True)),
                ("closed_deals_count", models.IntegerField(null=True)),
                ("activities_count", models.IntegerField(null=True)),
                ("done_activities_count", models.IntegerField(null=True)),
                ("undone_activities_count", models.IntegerField(null=True)),
                ("email_messages_count", models.IntegerField(null=True)),
                ("address", models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="OrganizationField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("key", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("field_type", models.CharField(max_length=255)),
                ("active_flag", models.NullBooleanField()),
                ("mandatory_flag", models.NullBooleanField()),
                ("edit_flag", models.NullBooleanField()),
                ("is_subfield", models.NullBooleanField()),
                (
                    "retrieved_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("last_updated_at", models.DateTimeField(null=True, blank=True)),
                ("name", models.CharField(max_length=255, null=True, blank=True)),
                ("phone", models.CharField(max_length=255, null=True, blank=True)),
                ("email", models.CharField(max_length=255, null=True, blank=True)),
                ("add_time", models.DateTimeField(null=True, blank=True)),
                ("update_time", models.DateTimeField(null=True, blank=True)),
                ("open_deals_count", models.IntegerField(null=True)),
                (
                    "visible_to",
                    models.IntegerField(
                        default=0, choices=[(0, b"private"), (3, b"shared")]
                    ),
                ),
                ("next_activity_date", models.DateField(null=True, blank=True)),
                ("next_activity_time", models.TimeField(null=True, blank=True)),
                ("last_activity_date", models.DateField(null=True, blank=True)),
                ("last_activity_time", models.TimeField(null=True, blank=True)),
                ("won_deals_count", models.IntegerField(null=True)),
                ("lost_deals_count", models.IntegerField(null=True)),
                ("closed_deals_count", models.IntegerField(null=True)),
                ("activities_count", models.IntegerField(null=True)),
                ("done_activities_count", models.IntegerField(null=True)),
                ("undone_activities_count", models.IntegerField(null=True)),
                ("email_messages_count", models.IntegerField(null=True)),
                (
                    "last_incoming_mail_time",
                    models.DateTimeField(null=True, blank=True),
                ),
                (
                    "last_outgoing_mail_time",
                    models.DateTimeField(null=True, blank=True),
                ),
                (
                    "org",
                    models.ForeignKey(
                        to_field=b"external_id",
                        blank=True,
                        to="pipedrive.Organization",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="PersonField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("key", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("field_type", models.CharField(max_length=255)),
                ("active_flag", models.NullBooleanField()),
                ("mandatory_flag", models.NullBooleanField()),
                ("edit_flag", models.NullBooleanField()),
                ("is_subfield", models.NullBooleanField()),
                (
                    "retrieved_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Pipeline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255, null=True, blank=True)),
                ("url_title", models.CharField(max_length=255, null=True, blank=True)),
                ("active", models.NullBooleanField()),
                ("add_time", models.DateTimeField(null=True, blank=True)),
                ("update_time", models.DateTimeField(null=True, blank=True)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Stage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                (
                    "pipeline_name",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("order_nr", models.IntegerField(null=True, blank=True)),
                ("active_flag", models.NullBooleanField()),
                ("update_time", models.DateTimeField(null=True, blank=True)),
                ("add_time", models.DateTimeField(null=True, blank=True)),
                (
                    "pipeline",
                    models.ForeignKey(
                        to_field=b"external_id",
                        blank=True,
                        to="pipedrive.Pipeline",
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(
                        db_index=True, unique=True, null=True, blank=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255, null=True, blank=True)),
                ("email", models.CharField(max_length=255, null=True, blank=True)),
                ("phone", models.CharField(max_length=255, null=True, blank=True)),
                ("last_login", models.DateTimeField(null=True, blank=True)),
                ("created", models.DateTimeField(null=True, blank=True)),
                ("modified", models.DateTimeField(null=True, blank=True)),
                ("role_id", models.IntegerField(null=True, blank=True)),
                ("active_flag", models.NullBooleanField()),
            ],
            options={"abstract": False},
        ),
        migrations.AddField(
            model_name="person",
            name="owner",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.User", null=True
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="owner",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.User", null=True
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="org",
            field=models.ForeignKey(
                to_field=b"external_id",
                blank=True,
                to="pipedrive.Organization",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="person",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.Person", null=True
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="user",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.User", null=True
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="creator_user",
            field=models.ForeignKey(
                related_name="creator",
                to_field=b"external_id",
                blank=True,
                to="pipedrive.User",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="org",
            field=models.ForeignKey(
                to_field=b"external_id",
                blank=True,
                to="pipedrive.Organization",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="person",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.Person", null=True
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="pipeline",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.Pipeline", null=True
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="user",
            field=models.ForeignKey(
                related_name="user",
                to_field=b"external_id",
                blank=True,
                to="pipedrive.User",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="deal",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.Deal", null=True
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="org",
            field=models.ForeignKey(
                to_field=b"external_id",
                blank=True,
                to="pipedrive.Organization",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="person",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.Person", null=True
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="user",
            field=models.ForeignKey(
                to_field=b"external_id", blank=True, to="pipedrive.User", null=True
            ),
        ),
    ]
