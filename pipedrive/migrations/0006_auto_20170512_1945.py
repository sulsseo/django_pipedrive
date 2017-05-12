# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pipedrive', '0005_auto_20170510_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 44, 45, 556137, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='deal',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 44, 54, 308044, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deal',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='dealfield',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 19, 283838, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dealfield',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='fieldmodification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 28, 235663, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fieldmodification',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 29, 963492, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 31, 531490, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='organizationfield',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 33, 331380, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizationfield',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 34, 747601, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='personfield',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 36, 91413, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personfield',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='pipeline',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 37, 547395, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pipeline',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 38, 963406, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stage',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 12, 19, 45, 40, 283309, tzinfo=utc), help_text=b'creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(help_text=b'edition date', auto_now=True, null=True),
        ),
    ]
