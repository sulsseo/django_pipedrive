# -*- encoding: utf-8 -*-

# standard library
import datetime
import pytz
import logging

# django
from django.db import models
from django.utils import timezone

# api
from pipedrive.pipedrive_client import PipedriveAPIClient

# utils
pipedrive_api_client = PipedriveAPIClient()

CREATOR_USER_ID = 2428657   # TestUser
PRIVATE = 0
SHARED = 3
VISIBILITY = (
    (PRIVATE, 'private'),   # Owner & followers
    (SHARED, 'shared'),     # Entire company
)


class PipedriveModel(models.Model):
    """
    Abstract class to include utility functions for extending classes.
    """

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
            time_string = str(el[date_fieldname]) + " " + str(el[time_fieldname])
            aware_date = timezone.make_aware(
                datetime.datetime.strptime(time_string + " UTC", "%Y-%m-%d %H:%M:%S %Z"),
                pytz.utc)
            return aware_date

    @classmethod
    def datetime_from_simple_time(cls, el, datetime_field):
        """
        The function takes a datetime_fieldname and
        returns a datetime aware of the timezone.
        Returns None if fields do not exist in el.
        """
        if datetime_field not in el or el[datetime_field] is None:
            return None
        else:
            return timezone.make_aware(
                datetime.datetime.strptime(el[datetime_field] + " UTC", "%Y-%m-%d %H:%M:%S %Z"),
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
    def get_str_or_none(cls, el, field_name):
        if field_name in el and el[field_name] is not None and el[field_name] != '':
            return el[field_name]
        return None

    @classmethod
    def fetch_from_pipedrive(cls):
        """
        The function iterates requesting for Organizations while in steps defined
        by Pipedrive while there is more items in the collection.
        """
        start = 0
        count_created = 0
        queries = 0

        while True:

            post_data = cls.get_api_call(start=start)

            # Error code from the API
            if not post_data['success']:
                logging.error(post_data[u'error'])
                return False

            # For each element from the request
            for el in post_data['data']:

                # update or create a local Entity
                entity, created = cls.update_or_create_entity_from_api_post(el)

                # update counters
                queries = queries + 1
                if created:
                    count_created = count_created + 1

            additional_data = post_data['additional_data']

            # Break the loop when the API replies there is no more pagination
            if 'pagination' not in additional_data or not additional_data['pagination']['more_items_in_collection']:
                break

            start = additional_data['pagination']['next_start']

        # report
        logging.info("Queries: " + str(queries))
        logging.info("Entities created: " + str(count_created))
        logging.info("Entities updated: " + str(queries - count_created))

        return True

    def upload(self):

        kwargs = self.build_kwargs()

        post_data = self.post_api_call(kwargs)

        self.external_id = post_data['data']['id']
        self.last_updated_at = timezone.now()
        self.save()

        self.__class__.update_or_create_entity_from_api_post(post_data[u'data'])
        return True


class User(PipedriveModel):
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=255,
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

    @classmethod
    def get_api_call(cls, start):
        return pipedrive_api_client.get_users(start=start)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
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
            }
        )


class Organization(PipedriveModel):
    """
    saves a registry of Org sent to pipedrive
    """
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    owner_id = models.IntegerField(
        null=True
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
    next_activity_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_activity_datetime = models.DateTimeField(
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
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return str(self.external_id) + " : " + str(self.name)

    @classmethod
    def get_api_call(cls, start):
        return pipedrive_api_client.get_organizations(start=start)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
        return Organization.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'owner_id': el[u'owner_id'][u'id'],
                'people_count': el[u'people_count'],
                'open_deals_count': el[u'open_deals_count'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'visible_to': el[u'visible_to'],
                'next_activity_datetime':
                    cls.datetime_from_fields(
                        el, u'next_activity_date', u'next_activity_time'),
                'last_activity_datetime':
                    cls.datetime_from_fields(
                        el, u'last_activity_date', u'last_activity_time'),
                'won_deals_count': el[u'won_deals_count'],
                'lost_deals_count': el[u'lost_deals_count'],
                'closed_deals_count': el[u'closed_deals_count'],
                'activities_count': el[u'activities_count'],
                'done_activities_count': el[u'done_activities_count'],
                'undone_activities_count': el[u'undone_activities_count'],
                'email_messages_count': el[u'email_messages_count'],
                'address': el[u'address_formatted_address'],
            }
        )

    def build_kwargs(self):
        return {
            'name': self.name
        }

    def post_api_call(self, kwargs):
        return pipedrive_api_client.post_organization(**kwargs)


class Person(PipedriveModel):
    """
    saves a registry of Person sent to pipedrive
    """
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    email = models.CharField(
        max_length=255,
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
    owner_id = models.IntegerField(
        null=True,
    )
    open_deals_count = models.IntegerField(
        null=True,
    )
    visible_to = models.IntegerField(
        default=0,
        choices=VISIBILITY
    )
    next_activity_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_activity_datetime = models.DateTimeField(
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

    def __unicode__(self):
        return str(self.external_id) + " : " + str(self.name)

    @classmethod
    def get_api_call(cls, start):
        return pipedrive_api_client.get_persons(start=start)

    @classmethod
    def post_api_call(cls, kwargs):
        return pipedrive_api_client.post_person(**kwargs)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
        return Person.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'name': el[u'name'],
                'phone': cls.get_primary(el, u'phone'),
                'email': cls.get_primary(el, u'email'),
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'org_id': cls.get_internal_field(el, u'org_id', u'value'),
                'owner_id': el[u'owner_id'][u'id'],
                'open_deals_count': el[u'open_deals_count'],
                'visible_to': el[u'visible_to'],
                'next_activity_datetime':
                    cls.datetime_from_fields(
                        el, u'next_activity_date', u'next_activity_time'),
                'last_activity_datetime':
                    cls.datetime_from_fields(
                        el, u'last_activity_date', u'last_activity_time'),
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
                    el, u'last_outgoing_mail_time')
            }
        )

    def build_kwargs(self):
        return {
            'name': self.name
        }


class Deal(PipedriveModel):
    """
    saves a registry of deal sent to pipedrive
    """
    title = models.CharField(
        max_length=255,
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
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )
    last_updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    creator_user_id = models.IntegerField(
        null=True
    )
    external_user_id = models.IntegerField(
        null=True
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
    external_pipeline_id = models.IntegerField(
        null=True
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
    next_activity_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_activity_datetime = models.DateTimeField(
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
    lost_reason = models.CharField(
        max_length=255,
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

    def __unicode__(self):
        return str(self.external_id) + " : " + str(self.title)

    @classmethod
    def get_api_call(cls, start):
        return pipedrive_api_client.get_deals(start=start)

    @classmethod
    def post_api_call(cls, kwargs):
        return pipedrive_api_client.post_deal(**kwargs)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
        return Deal.objects.update_or_create(
            external_id=el[u'id'],
            defaults={
                'title': el[u'title'],
                'creator_user_id': cls.get_internal_field(el, 'creator_user_id', 'id'),
                'external_user_id': cls.get_internal_field(el, 'user_id', 'id'),
                'value': el[u'value'],
                'org_id': cls.get_internal_field(el, u'org_id', u'value'),
                'external_pipeline_id': el[u'pipeline_id'],
                'person_id': cls.get_internal_field(el, 'person_id', 'value'),
                'external_stage_id': el[u'stage_id'],
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'stage_change_time': cls.datetime_from_simple_time(el, u'stage_change_time'),
                'next_activity_datetime':
                    cls.datetime_from_fields(
                        el, u'next_activity_date', u'next_activity_time'),
                'last_activity_datetime':
                    cls.datetime_from_fields(
                        el, u'last_activity_date', u'last_activity_time'),
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
            }
        )

    def additional_fields_or_default(self, field_name, default_value=None):
        if field_name in self.additional_fields:
            return self.additional_fields[field_name]
        else:
            return default_value

    def build_kwargs(self):
        return {
            'title': self.title
        }


class BaseField(models.Model):
    """
    Stores a single field entry.
    :model:`pipeline.BaseField`.
    """

    external_id = models.IntegerField(
        null=True,
    )
    key = models.CharField(
        max_length=255,
    )
    name = models.CharField(
        max_length=255,
    )
    field_kind = models.CharField(
        max_length=255,
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


class OrganizationField(BaseField):
    """
    Stores a single organization field entry.
    :model:`pipeline.OrganizationField`.
    """

    def __unicode__(self):
        return u'External ID: {}, Name: {}, Key: {}.'.format(
            self.external_id, self.name, self.key)

    @classmethod
    def get_fields(cls):
        """
        Gets and stores all Org Fields from the api
        """
        raw_organizations = pipedrive_api_client.get_organization_fields()
        organization_fields = pipedrive_api_client.get_data_list(
            raw_organizations)

        for organization_field in organization_fields:

            fields_object, created = cls.objects.get_or_create(
                external_id=organization_field['id'],
                name=organization_field['name'],
            )

            if 'is_subfield' in organization_field:
                fields_object.is_subfield = True
            else:
                fields_object.is_subfield = False

            fields_object.key = organization_field['key']

            fields_object.field_kind = organization_field['field_type'],

            fields_object.active_flag = organization_field['active_flag'],

            fields_object.mandatory_flag = organization_field[
                'mandatory_flag'],

            fields_object.edit_flag = organization_field['edit_flag'],

            fields_object.save()


class DealField(BaseField):
    """
    Stores a single deal field entry.
    :model:`pipeline.DealField`.
    """

    def __unicode__(self):
        return u'External ID: {}, Name: {}, Key: {}.'.format(
            self.external_id, self.name, self.key)

    @classmethod
    def get_fields(cls):
        """
        Gets and stores all Org Fields from the api
        """
        raw_deals = pipedrive_api_client.get_deal_fields()
        deal_fields = pipedrive_api_client.get_data_list(raw_deals)

        for deal_field in deal_fields:

            fields_object, created = cls.objects.get_or_create(
                external_id=deal_field['id'],
                name=deal_field['name'],
            )

            if deal_field.get('is_subfield'):
                fields_object.is_subfield = deal_field['is_subfield']
            else:
                fields_object.is_subfield = False

            fields_object.key = deal_field['key']

            fields_object.field_kind = deal_field['field_type'],

            fields_object.active_flag = deal_field['active_flag'],

            fields_object.mandatory_flag = deal_field['mandatory_flag'],

            fields_object.edit_flag = deal_field['edit_flag'],

            fields_object.save()


class PersonField(BaseField):
    """
    Stores a single person field entry.
    :model:`pipeline.PersonField`.
    """

    def __unicode__(self):
        return u'External ID: {}, Name: {}, Key: {}.'.format(
            self.external_id, self.name, self.key)

    @classmethod
    def get_fields(cls):
        """
        Gets and stores all Org Fields from the api
        """
        raw_persons = pipedrive_api_client.get_person_fields()
        person_fields = pipedrive_api_client.get_data_list(raw_persons)

        for person_field in person_fields:

            fields_object, created = cls.objects.get_or_create(
                external_id=person_field['id'],
                name=person_field['name'],
            )

            if person_field.get('is_subfield'):
                fields_object.is_subfield = person_field['is_subfield']
            else:
                fields_object.is_subfield = False

            fields_object.key = person_field['key']

            fields_object.field_kind = person_field['field_type'],

            fields_object.active_flag = person_field['active_flag'],

            fields_object.mandatory_flag = person_field['mandatory_flag'],

            fields_object.edit_flag = person_field['edit_flag'],

            fields_object.save()


class Pipeline(models.Model):
    """
    Stores a single pipe line stage entry.
    :model:`pipeline.Pipeline`.
    """
    external_id = models.IntegerField(
    )
    name = models.CharField(
        max_length=255,
    )
    active_flag = models.BooleanField(
    )

    def __unicode__(self):
        return u'Pipe ID: {}, Name: {}.'.format(
            self.external_id, self.name)

    @classmethod
    def get_fields(cls):
        """
        Gets and stores all Org Fields from the api
        """
        raw_stages = pipedrive_api_client.get_pipeline_stages()
        pipeline_stages = pipedrive_api_client.get_data_list(raw_stages)

        for pipeline_stage in pipeline_stages:

            stage_object, created = cls.objects.get_or_create(
                external_id=pipeline_stage['id'],
                name=pipeline_stage['name'],
                active_flag=pipeline_stage['active']
            )


class Stage(models.Model):
    """
    Stores a single stage entry.
    :model:`pipeline.Stage`.
    """
    external_id = models.IntegerField(
    )
    pipeline_id = models.IntegerField(
    )
    pipeline_name = models.CharField(
        max_length=255,
    )
    name = models.CharField(
        max_length=255,
    )
    order_nr = models.IntegerField(
    )
    active_flag = models.BooleanField(
    )

    def __unicode__(self):
        return u'Stage ID: {}, Name: {}.'.format(
            self.external_id, self.name)

    @classmethod
    def get_fields(cls):
        """
        Gets and stores all Org Fields from the api
        """
        raw_stages = pipedrive_api_client.get_stages()
        stages = pipedrive_api_client.get_data_list(raw_stages)

        for stage in stages:

            stage_object, created = cls.objects.get_or_create(
                external_id=stage['id'],
                pipeline_id=stage['pipeline_id'],
                pipeline_name=stage['pipeline_name'],
                name=stage['name'],
                active_flag=stage['active_flag'],
                order_nr=stage['order_nr'],
            )


class Note(PipedriveModel):
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
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
    content = models.CharField(
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

    @classmethod
    def get_api_call(cls, start):
        return pipedrive_api_client.get_notes(start=start)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
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
            }
        )


class Activity(PipedriveModel):
    external_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
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
    subject = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    note = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=255,
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
    marked_as_done_time = models.TimeField(
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

    @classmethod
    def get_api_call(cls, start):
        return pipedrive_api_client.get_activities(start=start)

    @classmethod
    def update_or_create_entity_from_api_post(cls, el):
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
                'due_date': el[u'due_date'],
                'due_time': el[u'due_time'],
                'duration': el[u'duration'],
                'marked_as_done_time': cls.get_str_or_none(el, u'marked_as_done_time'),
                'add_time': cls.datetime_from_simple_time(el, u'add_time'),
                'update_time': cls.datetime_from_simple_time(el, u'update_time'),
                'active_flag': el[u'active_flag'],
            }
        )
