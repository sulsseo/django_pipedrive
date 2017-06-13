# -*- encoding: utf-8 -*-

# standard library
import datetime
import pytz
import logging
import copy
from collections import defaultdict

# django
from django.db import models
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# postgres
from django.contrib.postgres.fields import HStoreField

# api
from pipedrive.pipedrive_client import PipedriveAPIClient

from pipedrive.utils import compare_dicts
from fields import TruncatingCharField

PRIVATE = 0
SHARED = 3
VISIBILITY = (
    (PRIVATE, 'private'),   # Owner & followers
    (SHARED, 'shared'),     # Entire company
)


class UnableToSyncException(Exception):
    def __init__(self, model, external_id):
        self.external_id = external_id
        self.model = model


class BaseModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="creation date",
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True,
        help_text="edition date",
    )

    class Meta:
        """ set to abstract """
        abstract = True

    def update(self, commit=True, **kwargs):
        """ proxy method for the QuerySet: update method
        highly recommended when you need to save just one field

        """
        kwargs['updated_at'] = timezone.now()

        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])

        if commit:
            self.__class__.objects.filter(pk=self.pk).update(**kwargs)


class FieldModification(BaseModel):
    field_name = TruncatingCharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    previous_value = TruncatingCharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    current_value = TruncatingCharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    created = models.DateTimeField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):              # __unicode__ on Python 2
        return u"{}[{}] changed field '{}' from {} to {}".format(
            self.content_type,
            self.object_id,
            self.field_name,
            self.previous_value,
            self.current_value
        )

    @classmethod
    def create_modifications(cls, instance, previous, current):

        prev = defaultdict(lambda: None, previous)
        curr = defaultdict(lambda: None, current)

        # Compute difference between previous and current
        diffkeys = set([k for k in prev if prev[k] != curr[k]])
        in_previous_not_current = set([k for k in prev if k not in curr])
        in_current_not_previous = set([k for k in curr if k not in prev])

        diffkeys = diffkeys.union(in_previous_not_current).union(in_current_not_previous)
        current_datetime = datetime.datetime.now()

        for key in diffkeys:
            FieldModification.objects.create(
                field_name=key,
                previous_value=prev[key],
                current_value=curr[key],
                content_object=instance,
                created=current_datetime,
            )


class PipedriveModel(BaseModel):
    """
    Abstract class to include utility functions for extending classes.
    """

    additional_fields = HStoreField(
        null=True,
    )
    modifications = GenericRelation(FieldModification)

    content_type = models.ForeignKey(
        ContentType,
        null=True,
    )
    object_id = models.PositiveIntegerField(
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

    @classmethod
    def datetime_from_fields(cls, el, date_fieldname, time_fieldname):
        """
        The function takes a date_fieldname and a time_fieldname
        and puts them together as a datetime aware of the timezone.
        Returns None if fields do not exist in el.
        """
        if date_fieldname not in el or el[date_fieldname] is None:
            return None
        else:
            time_string = u"{} {}".format(el[date_fieldname], el[time_fieldname])
            aware_date = timezone.make_aware(
                datetime.datetime.strptime(u"{} UTC".format(time_string), "%Y-%m-%d %H:%M:%S %Z"),
                pytz.utc)
            return aware_date

    @classmethod
    def datetime_from_simple_time(cls, el, datetime_field):
        """
        The function takes a datetime_fieldname and
        returns a datetime aware of the timezone.
        Returns None if fields do not exist in el.
        """
        if (datetime_field not in el or
            el[datetime_field] is None or
            el[datetime_field] == '0000-00-00 00:00:00' or
                el[datetime_field] == ''):

            return None
        else:
            return timezone.make_aware(
                datetime.datetime.strptime(u"{} UTC".format(el[datetime_field]), "%Y-%m-%d %H:%M:%S %Z"),
                pytz.utc)

    @classmethod
    def get_primary(cls, el, field_name):
        if field_name not in el:
            return None
        result = filter(lambda x: x[u'primary'], el[field_name])
        if result:
            return result[0][u'value']
        else:
            return None

    @classmethod
    def get_internal_field(cls, el, first_field_name, second_field_name):
        if first_field_name in el and el[first_field_name] is not None:
            return el[first_field_name][second_field_name]
        return None

    @classmethod
    def get_id(cls, el, field_name):
        if field_name in el and isinstance(el[field_name], int):
            return el[field_name]
        return cls.get_internal_field(el, field_name, u'value')

    @classmethod
    def get_value_or_none(cls, el, field_name):
        if field_name in el and el[field_name] is not None and el[field_name] != '':
            return el[field_name]
        return None

    @classmethod
    def sync_one(cls, external_id):
        post_data = cls.pipedrive_api_client.get_instance(external_id)

        # Error code from the API
        if not post_data[u'success']:
            logging.error(post_data[u'error'])
            raise UnableToSyncException(cls, external_id)

        return cls.update_or_create_entity_from_api_post(post_data[u'data'])

    @classmethod
    def get_table_fields(cls):
        table_fields = set()

        for field in cls._meta.get_fields(include_parents=True):
            if field.concrete and field.attname != u'id':
                table_fields.add(field.attname)

        return table_fields

    @classmethod
    def handle_dependencies(cls, el, e):
        creator_user_id = cls.get_id(el, u'creator_user_id')
        user_id = cls.get_id(el, u'user_id')
        person_id = cls.get_id(el, u'person_id')
        org_id = cls.get_id(el, u'org_id')
        stage_id = cls.get_id(el, u'stage_id')
        pipeline_id = cls.get_id(el, u'pipeline_id')
        deal_id = cls.get_id(el, u'deal_id')
        activity_id = cls.get_id(el, u'activity_id')
        note_id = cls.get_id(el, u'note_id')

        if creator_user_id:
            User.sync_one(creator_user_id)
        if user_id:
            User.sync_one(user_id)
        if org_id:
            Organization.sync_one(org_id)
        if pipeline_id:
            Pipeline.sync_one(pipeline_id)
        if stage_id:
            Stage.sync_one(stage_id)
        if person_id:
            Person.sync_one(person_id)
        if deal_id:
            Deal.sync_one(deal_id)
        if activity_id:
            Activity.sync_one(activity_id)
        if note_id:
            Note.sync_one(note_id)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
        """
        The method computes which fields go to additional_fields by getting
        all keys from @el which are not fields in the model's table.
        """
        table_fields = cls.get_table_fields()

        additional_fields = {}

        for key in el.iterkeys():
            if key not in table_fields:
                additional_fields[key] = unicode(el[key])

        entity, created = cls.update_or_create_entity_with_additional_fields(el, additional_fields)
        # Force save for signals
        entity.save()
        return entity, created

    @classmethod
    def fetch_from_pipedrive(cls):
        """
        The function iterates requesting for Organizations while in steps defined
        by Pipedrive while there is more items in the collection.
        """
        start = 0
        count_created = 0
        queries = 0
        problems_solved = 0
        logging.info(u"Fetching model {} from pipedrive".format(cls))
        previous_post_data = {}
        while True:

            post_data = cls.pipedrive_api_client.get_instances(start=start)

            post_copy = copy.copy(post_data)
            post_copy.pop('additional_data', None)

            if compare_dicts(previous_post_data, post_copy):
                logging.warn("Same post_data as previous request")
                return False

            previous_post_data = post_copy

            # Error code from the API
            if not post_data['success']:
                logging.error(post_data[u'error'])
                return False

            # No data available
            if post_data['data'] is None:
                return True

            # For each element from the request
            for el in post_data['data']:

                try:
                    # update or create a local Entity
                    entity, created = cls.update_or_create_entity_from_api_post(el)

                    # update counters
                    queries = queries + 1
                    if created:
                        count_created = count_created + 1

                except IntegrityError as e:
                    logging.warning(e)
                    cls.handle_dependencies(el, e)

                    # try again to update or create a local Entity
                    entity, created = cls.update_or_create_entity_from_api_post(el)

                    if created:
                        problems_solved = problems_solved + 1

            # Break the loop when there is no pagination info
            if 'additional_data' not in post_data:
                break

            additional_data = post_data['additional_data']

            # Break the loop when the API replies there is no more pagination
            if ('pagination' not in additional_data or
                    not additional_data['pagination']['more_items_in_collection']):
                break

            start = additional_data['pagination']['next_start']

        # report
        logging.info(u"Queries: {}".format(queries))
        logging.info(u"Entities created: {}".format(count_created))
        logging.info(u"Entities updated: {}".format(queries - count_created))
        logging.info(u"Problems solved: {}".format(problems_solved))

        return True

    @classmethod
    def sync_from_pipedrive(cls):
        result = User.fetch_from_pipedrive()
        result = result and PersonField.fetch_from_pipedrive()
        result = result and OrganizationField.fetch_from_pipedrive()
        result = result and DealField.fetch_from_pipedrive()

        # TODO: wait for the API to implement properly
        Pipeline.fetch_from_pipedrive()

        result = result and Stage.fetch_from_pipedrive()
        result = result and Organization.fetch_from_pipedrive()
        result = result and Person.fetch_from_pipedrive()
        result = result and Deal.fetch_from_pipedrive()
        result = result and Note.fetch_from_pipedrive()
        result = result and Activity.fetch_from_pipedrive()
        return result

    RESERVED_NAMES = [
        u'id',
        u'next_activity',
        u'last_activity',
        u'cc_email',
        u'owner_name',
        u'edit_name',
    ]

    def upload(self):

        kwargs = self.build_kwargs()

        # Filter keys not changeable by API
        kwargs = {k: v for k, v in kwargs.iteritems() if k not in PipedriveModel.RESERVED_NAMES}

        if self.external_id is None:
            post_data = self.pipedrive_api_client.post_instance(**kwargs)
        else:
            post_data = self.pipedrive_api_client.update(self.external_id, **kwargs)

        if not post_data[u'success']:
            logging.error(post_data)
            return False

        self.external_id = post_data['data']['id']
        self.last_updated_at = timezone.now()
        self.save()

        entity, created = self.__class__.update_or_create_entity_from_api_post(post_data[u'data'])

        # Attributes from the newly created object are copied to self
        for field in self.__class__._meta.get_fields(include_parents=True):
            if field.concrete and field.attname != u'id':
                if field.concrete:
                    setattr(self, field.attname, getattr(entity, field.attname))

        return True


class User(PipedriveModel):

    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        unique=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    name = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    email = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    phone = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        null=True,
        blank=True,
    )
    modified = models.DateTimeField(
        null=True,
        blank=True,
    )
    role_id = models.IntegerField(
        null=True,
        blank=True,
    )
    active_flag = models.NullBooleanField(
        null=True
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='users')

    def build_kwargs(self):
        return {
            'id': self.external_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'last_login': self.last_login,
            'created': self.created,
            'modified': self.modified,
            'role_id': self.role_id,
            'active_flag': self.active_flag,
        }

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return User.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'email': el[u'email'],
                'phone': el[u'phone'],
                'last_login': cls.datetime_from_simple_time(el, u'last_login'),
                'created': cls.datetime_from_simple_time(el, u'created'),
                'modified': cls.datetime_from_simple_time(el, u'modified'),
                'role_id': el[u'role_id'],
                'active_flag': el[u'active_flag'],
                'additional_fields': additional_fields,
            }
        )


class Pipeline(PipedriveModel):
    """
    Stores a single pipe line stage entry.
    :model:`pipeline.Pipeline`.
    """
    external_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    name = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    url_title = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    active = models.NullBooleanField(
        null=True,
        blank=True,
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='pipelines')

    def build_kwargs(self):
        return {
            'id': self.external_id,
            'name': self.name,
            'url_title': self.url_title,
            'active': self.active,
            'add_time': self.add_time,
            'update_time': self.update_time,
        }

    def __unicode__(self):
        return u'Pipe ID: {}, Name: {}.'.format(
            self.external_id, self.name)

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Pipeline.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'url_title': el[u'url_title'],
                'active': el[u'active'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'active': el[u'active'],
                'additional_fields': additional_fields,
            }
        )


class Organization(PipedriveModel):
    """
    saves a registry of Org sent to pipedrive
    """
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        unique=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    name = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        to_field="external_id",
    )
    people_count = models.IntegerField(
        null=True
    )
    open_deals_count = models.IntegerField(
        null=True
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    visible_to = models.IntegerField(
        default=0,
        choices=VISIBILITY
    )
    next_activity_date = models.DateField(
        null=True,
        blank=True,
    )
    next_activity_time = models.TimeField(
        null=True,
        blank=True,
    )
    last_activity_date = models.DateField(
        null=True,
        blank=True,
    )
    last_activity_time = models.TimeField(
        null=True,
        blank=True,
    )
    won_deals_count = models.IntegerField(
        null=True
    )
    lost_deals_count = models.IntegerField(
        null=True
    )
    closed_deals_count = models.IntegerField(
        null=True
    )
    activities_count = models.IntegerField(
        null=True
    )
    done_activities_count = models.IntegerField(
        null=True
    )
    undone_activities_count = models.IntegerField(
        null=True
    )
    email_messages_count = models.IntegerField(
        null=True
    )
    address = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='organizations')

    def build_kwargs(self):

        kwargs = {
            'id': self.external_id,
            'name': self.name,
            'visible_to': self.visible_to,
            'address': self.address,
        }

        additional_fields = self.additional_fields

        if additional_fields:
            for key, value in additional_fields.iteritems():
                kwargs[key] = value

        return kwargs

    def __unicode__(self):
        return "{} : {}".format(self.external_id, self.name)

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Organization.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'owner_id': cls.get_id(el, u'owner_id'),
                'people_count': el[u'people_count'],
                'open_deals_count': el[u'open_deals_count'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'visible_to': el[u'visible_to'],
                'next_activity_date': cls.get_value_or_none(el, u'next_activity_date'),
                'next_activity_time': cls.get_value_or_none(el, u'next_activity_time'),
                'last_activity_date': cls.get_value_or_none(el, u'last_activity_date'),
                'last_activity_time': cls.get_value_or_none(el, u'last_activity_time'),
                'won_deals_count': el[u'won_deals_count'],
                'lost_deals_count': el[u'lost_deals_count'],
                'closed_deals_count': el[u'closed_deals_count'],
                'activities_count': el[u'activities_count'],
                'done_activities_count': el[u'done_activities_count'],
                'undone_activities_count': el[u'undone_activities_count'],
                'email_messages_count': el[u'email_messages_count'],
                'address': el[u'address_formatted_address'],
                'additional_fields': additional_fields,
            }
        )


class Person(PipedriveModel):
    """
    saves a registry of Person sent to pipedrive
    """
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        unique=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    name = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    phone = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    email = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    org = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        to_field="external_id",
    )
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        to_field="external_id",
    )
    open_deals_count = models.IntegerField(
        null=True,
    )
    visible_to = models.IntegerField(
        default=0,
        choices=VISIBILITY
    )
    next_activity_date = models.DateField(
        null=True,
        blank=True,
    )
    next_activity_time = models.TimeField(
        null=True,
        blank=True,
    )
    last_activity_date = models.DateField(
        null=True,
        blank=True,
    )
    last_activity_time = models.TimeField(
        null=True,
        blank=True,
    )
    won_deals_count = models.IntegerField(
        null=True
    )
    lost_deals_count = models.IntegerField(
        null=True
    )
    closed_deals_count = models.IntegerField(
        null=True
    )
    activities_count = models.IntegerField(
        null=True
    )
    done_activities_count = models.IntegerField(
        null=True
    )
    undone_activities_count = models.IntegerField(
        null=True
    )
    email_messages_count = models.IntegerField(
        null=True
    )
    last_incoming_mail_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_outgoing_mail_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='persons')

    def build_kwargs(self):

        kwargs = {
            'id': self.external_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'org_id': self.org_id,
        }

        additional_fields = self.additional_fields

        if additional_fields:
            for key, value in additional_fields.iteritems():
                kwargs[key] = value

        return kwargs

    def __unicode__(self):
        return "{} : {}".format(self.external_id, self.name)

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Person.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'phone': cls.get_primary(el, u'phone'),
                'email': cls.get_primary(el, u'email'),
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'org_id': cls.get_id(el, u'org_id'),
                'owner_id': cls.get_id(el, u'owner_id'),
                'open_deals_count': el[u'open_deals_count'],
                'visible_to': el[u'visible_to'],
                'next_activity_date': cls.get_value_or_none(el, u'next_activity_date'),
                'next_activity_time': cls.get_value_or_none(el, u'next_activity_time'),
                'last_activity_date': cls.get_value_or_none(el, u'last_activity_date'),
                'last_activity_time': cls.get_value_or_none(el, u'last_activity_time'),
                'won_deals_count': el[u'won_deals_count'],
                'lost_deals_count': el[u'lost_deals_count'],
                'closed_deals_count': el[u'closed_deals_count'],
                'activities_count': el[u'activities_count'],
                'done_activities_count': el[u'done_activities_count'],
                'undone_activities_count': el[u'undone_activities_count'],
                'email_messages_count': el[u'email_messages_count'],
                'last_incoming_mail_time': cls.datetime_from_simple_time(
                    el, u'last_incoming_mail_time'),
                'last_outgoing_mail_time': cls.datetime_from_simple_time(
                    el, u'last_outgoing_mail_time'),
                'additional_fields': additional_fields,
            }
        )


class Deal(PipedriveModel):

    """
    saves a registry of deal sent to pipedrive
    """
    title = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    upload_timestamp = models.DateTimeField(
        null=True,
        blank=True,
    )
    person = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
    )
    stage = models.ForeignKey(
        'Stage',
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
    )
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        unique=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    status = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
        related_name='user'
    )
    creator_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
        related_name='creator'
    )
    value = models.IntegerField(
        null=True
    )
    org = models.ForeignKey(
        'Organization',
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
    )
    pipeline = models.ForeignKey(
        Pipeline,
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
    )

    external_stage_id = models.IntegerField(
        null=True
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    stage_change_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    next_activity_date = models.DateField(
        null=True,
        blank=True,
    )
    next_activity_time = models.TimeField(
        null=True,
        blank=True,
    )
    last_activity_date = models.DateField(
        null=True,
        blank=True,
    )
    last_activity_time = models.TimeField(
        null=True,
        blank=True,
    )
    won_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_incoming_mail_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_outgoing_mail_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    lost_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    close_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    lost_reason = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    visible_to = models.IntegerField(
        default=0,
        choices=VISIBILITY
    )
    activities_count = models.IntegerField(
        null=True
    )
    done_activities_count = models.IntegerField(
        null=True
    )
    undone_activities_count = models.IntegerField(
        null=True
    )
    email_messages_count = models.IntegerField(
        null=True
    )
    expected_close_date = models.DateField(
        null=True,
        blank=True,
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='deals')

    def build_kwargs(self):

        kwargs = {
            'id': self.external_id,
            'title': self.title,
            'value': self.value,
            'pipeline_id': self.pipeline_id,
            'visible_to': self.visible_to,
            'person_id': self.person_id,
            'org_id': self.org_id,
            'user_id': self.user_id,
            'stage_id': self.stage_id,
            'status': self.status,
            'lost_reason': self.lost_reason,
        }

        additional_fields = self.additional_fields

        if additional_fields:
            for key, value in additional_fields.iteritems():
                kwargs[key] = value

        return kwargs

    def __unicode__(self):
        return "{} : {}".format(self.external_id, self.title)

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Deal.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'title': el[u'title'],
                'creator_user_id': cls.get_id(el, 'creator_user_id'),
                'user_id': cls.get_id(el, 'user_id'),
                'value': el[u'value'],
                'org_id': cls.get_id(el, u'org_id'),
                'pipeline_id': el[u'pipeline_id'],
                'person_id': cls.get_id(el, 'person_id'),
                'external_stage_id': el[u'stage_id'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'stage_change_time': cls.datetime_from_simple_time(el, u'stage_change_time'),
                'next_activity_date': cls.get_value_or_none(el, u'next_activity_date'),
                'next_activity_time': cls.get_value_or_none(el, u'next_activity_time'),
                'last_activity_date': cls.get_value_or_none(el, u'last_activity_date'),
                'last_activity_time': cls.get_value_or_none(el, u'last_activity_time'),
                'won_time': cls.datetime_from_simple_time(el, u'won_time'),
                'last_incoming_mail_time':
                    cls.datetime_from_simple_time(el, u'last_incoming_mail_time'),
                'last_outgoing_mail_time':
                    cls.datetime_from_simple_time(el, u'last_outgoing_mail_time'),
                'lost_time': cls.datetime_from_simple_time(el, u'lost_time'),
                'close_time': cls.datetime_from_simple_time(el, u'close_time'),
                'lost_reason': el[u'lost_reason'],
                'visible_to': el[u'visible_to'],
                'activities_count': el[u'activities_count'],
                'done_activities_count': el[u'done_activities_count'],
                'undone_activities_count': el[u'undone_activities_count'],
                'email_messages_count': el[u'email_messages_count'],
                'expected_close_date': el[u'expected_close_date'],
                'additional_fields': additional_fields,
            }
        )

    def additional_fields_or_default(self, field_name, default_value=None):
        if field_name in self.additional_fields:
            return self.additional_fields[field_name]
        else:
            return default_value


class BaseField(PipedriveModel):
    """
    Stores a single field entry.
    :model:`pipeline.BaseField`.
    """

    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        unique=True,
    )
    key = TruncatingCharField(
        max_length=500,
    )
    name = TruncatingCharField(
        max_length=500,
    )
    field_type = TruncatingCharField(
        max_length=500,
    )
    active_flag = models.NullBooleanField(
        null=True,
    )
    mandatory_flag = models.NullBooleanField(
        null=True,
    )
    edit_flag = models.NullBooleanField(
        null=True,
    )
    is_subfield = models.NullBooleanField(
        null=True,
    )
    retrieved_time = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'External ID: {}, Name: {}, Key: {}.'.format(
            self.external_id, self.name, self.key)

    def build_kwargs(self):
        return {
            'id': self.external_id,
            'name': self.name,
            'field_type': self.field_type,
        }

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
        obj, created = cls.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'key': el[u'key'],
                'field_type': el[u'field_type'],
                'active_flag': el[u'active_flag'],
                'mandatory_flag': el[u'mandatory_flag'],
                'edit_flag': el[u'edit_flag'],
            }
        )
        obj.save()
        return obj, created


class OrganizationField(BaseField):
    """
    Stores a single organization field entry.
    :model:`pipeline.OrganizationField`.
    """

    pipedrive_api_client = PipedriveAPIClient(endpoint='organizationFields')


class DealField(BaseField):
    """
    Stores a single deal field entry.
    :model:`pipeline.DealField`.
    """

    pipedrive_api_client = PipedriveAPIClient(endpoint='dealFields')


class PersonField(BaseField):
    """
    Stores a single person field entry.
    :model:`pipeline.PersonField`.
    """

    pipedrive_api_client = PipedriveAPIClient(endpoint='personFields')


class Stage(PipedriveModel):
    """
    Stores a single stage entry.
    :model:`pipeline.Stage`.
    """
    external_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    pipeline = models.ForeignKey(
        Pipeline,
        null=True,
        blank=True,
        db_index=True,
        to_field="external_id",
    )
    pipeline_name = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    name = TruncatingCharField(
        max_length=500,
    )
    order_nr = models.IntegerField(
        null=True,
        blank=True,
    )
    active_flag = models.NullBooleanField(
        null=True
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='stages')

    def build_kwargs(self):
        return {
            'id': self.external_id,
            'name': self.name,
            'pipeline_id': self.pipeline_id,
            'order_nr': self.order_nr,
            'active_flag': self.active_flag,
        }

    def __unicode__(self):
        return u'Stage ID: {}, Name: {}.'.format(
            self.external_id, self.name)

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Stage.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'pipeline_id': el[u'pipeline_id'],
                'pipeline_name': cls.get_value_or_none(el, u'pipeline_name'),
                'name': el[u'name'],
                'order_nr': el[u'order_nr'],
                'active_flag': el[u'active_flag'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'additional_fields': additional_fields,
            }
        )


class Note(PipedriveModel):
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        to_field="external_id",
    )
    deal = models.ForeignKey(
        Deal,
        null=True,
        blank=True,
        to_field="external_id",
    )
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        to_field="external_id",
    )
    org = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        to_field="external_id",
    )
    content = TruncatingCharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    active_flag = models.NullBooleanField(
        null=True
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='notes')

    def __unicode__(self):
        return u"{} : {}".format(self.external_id, self.content)

    def build_kwargs(self):
        return {
            'id': self.external_id,
            'content': self.content,
            'active_flag': self.active_flag,
            'deal_id': self.deal_id,
            'person_id': self.person_id,
            'org_id': self.org_id,
        }

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Note.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'user_id': el[u'user_id'],
                'deal_id': el[u'deal_id'],
                'person_id': el[u'person_id'],
                'org_id': el[u'org_id'],
                'content': el[u'content'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'active_flag': el[u'active_flag'],
                'additional_fields': additional_fields,
            }
        )


class Activity(PipedriveModel):
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
    )
    deleted = models.BooleanField(
        default=False
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        to_field="external_id",
    )
    deal = models.ForeignKey(
        Deal,
        null=True,
        blank=True,
        to_field="external_id",
    )
    org = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        to_field="external_id",
    )
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        to_field="external_id",
    )
    done = models.NullBooleanField(
        null=True
    )
    subject = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    note = TruncatingCharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    type = TruncatingCharField(
        max_length=500,
        null=True,
        blank=True,
    )
    due_date = models.DateField(
        null=True,
        blank=True,
    )
    due_time = models.TimeField(
        null=True,
        blank=True,
    )
    duration = models.TimeField(
        null=True,
        blank=True,
    )
    marked_as_done_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    active_flag = models.NullBooleanField(
        null=True
    )
    update_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    add_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    pipedrive_api_client = PipedriveAPIClient(endpoint='activities')

    def build_kwargs(self):
        return {
            'id': self.external_id,
            'done': self.done,
            'subject': self.subject,
            'note': self.note,
            'type': self.type,
            'due_date': self.due_date,
            'due_time': self.due_time,
            'marked_as_done_time': self.marked_as_done_time,
            'active_flag': self.active_flag,
        }

    @classmethod
    def update_or_create_entity_with_additional_fields(cls, el, additional_fields):
        return Activity.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'user_id': el[u'user_id'],
                'deal_id': el[u'deal_id'],
                'person_id': el[u'person_id'],
                'org_id': el[u'org_id'],
                'subject': el[u'subject'],
                'note': el[u'note'],
                'done': el[u'done'],
                'type': el[u'type'],
                'due_date': cls.get_value_or_none(el, u'due_date'),
                'due_time': cls.get_value_or_none(el, u'due_time'),
                'duration': cls.get_value_or_none(el, u'duration'),
                'marked_as_done_time': cls.datetime_from_simple_time(el, u'marked_as_done_time'),
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'active_flag': el[u'active_flag'],
                'additional_fields': additional_fields,
            }
        )
