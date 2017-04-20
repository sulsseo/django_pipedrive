# Create your tests here.

import pytz
import datetime
import json

from django.test import TestCase
from django.test import Client

from pipedrive.models import Deal
from pipedrive.models import Person
from pipedrive.models import Organization
from pipedrive.models import PersonField
from pipedrive.models import DealField
from pipedrive.models import OrganizationField
from pipedrive.models import Pipeline
from pipedrive.models import Stage


class TestPipedriveWebhooks(TestCase):

    def test_update_deal(self):
        c = Client()

        deal = Deal.objects.create(
            title="TEST_DEAL",
            external_id=999,
            value=0,
        )

        self.assertEquals(Deal.objects.count(), 1)

        data = {
            "v":1,
            "matches_filters":
                {
                    "current":[],
                    "previous":[]
                },
            "meta": 
                {
                    "v":1,
                    "action":"updated",
                    "object":"deal",
                    "id":999,
                    "company_id":1689563,
                    "user_id":2428657,
                    "host":"mycompany.pipedrive.com",
                    "timestamp":1492636837,
                    "timestamp_milli":1492636837696,
                    "permitted_user_ids":[2428657],
                    "trans_pending":False,
                    "is_bulk_update":False,
                    "elastic_enabled":True,
                    "matches_filters":{"current":[],
                    "previous":[]}
                },
            "retry":0,
            "current":
                {
                    "id":999,
                    "creator_user_id":2428657,
                    "user_id":2428657,
                    "person_id":None,
                    "org_id":None,
                    "stage_id":1,
                    "title":"TEST_DEAL",
                    "value":1000,
                    "currency":"USD",
                    "add_time":"2017-04-19 19:43:40",
                    "update_time":"2017-04-19 21:20:37",
                    "stage_change_time":None,
                    "active":True,
                    "deleted":False,
                    "status":"open",
                    "next_activity_date":None,
                    "next_activity_time":None,
                    "next_activity_id":None,
                    "last_activity_id":None,
                    "last_activity_date":None,
                    "lost_reason":None,
                    "visible_to":"3",
                    "close_time":None,
                    "pipeline_id":1,
                    "won_time":None,
                    "first_won_time":None,
                    "lost_time":None,
                    "products_count":0,
                    "files_count":0,
                    "notes_count":0,
                    "followers_count":1,
                    "email_messages_count":0,
                    "activities_count":0,
                    "done_activities_count":0,
                    "undone_activities_count":0,
                    "reference_activities_count":0,
                    "participants_count":0,
                    "expected_close_date":None,
                    "last_incoming_mail_time":None,
                    "last_outgoing_mail_time":None,
                    "stage_order_nr":1,
                    "person_name":None,
                    "org_name":None,
                    "next_activity_subject":None,
                    "next_activity_type":None,
                    "next_activity_duration":None,
                    "next_activity_note":None,
                    "formatted_value":"1 000 $",
                    "rotten_time":None,
                    "weighted_value":1000,
                    "formatted_weighted_value":"1 000 $",
                    "owner_name":"TEST_owner",
                    "cc_email":"mycompany+deal2@pipedrivemail.com",
                    "org_hidden":False,
                    "person_hidden":False
                },
            "previous":
                {
                    "id":999,
                    "creator_user_id":2428657,
                    "user_id":2428657,
                    "person_id":None,
                    "org_id":None,
                    "stage_id":1,
                    "title":"TEST_DEAL",
                    "value":0,
                    "currency":"USD",
                    "add_time":"2017-04-19 19:43:40",
                    "update_time":"2017-04-19 19:43:41",
                    "stage_change_time":None,
                    "active":True,
                    "deleted":False,
                    "status":"open",
                    "next_activity_date":None,
                    "next_activity_time":None,
                    "next_activity_id":None,
                    "last_activity_id":None,
                    "last_activity_date":None,
                    "lost_reason":None,
                    "visible_to":"3",
                    "close_time":None,
                    "pipeline_id":1,
                    "won_time":None,
                    "first_won_time":None,
                    "lost_time":None,
                    "products_count":0,
                    "files_count":0,
                    "notes_count":0,
                    "followers_count":1,
                    "email_messages_count":0,
                    "activities_count":0,
                    "done_activities_count":0,
                    "undone_activities_count":0,
                    "reference_activities_count":0,
                    "participants_count":0,
                    "expected_close_date":None,
                    "last_incoming_mail_time":None,
                    "last_outgoing_mail_time":None,
                    "stage_order_nr":1,
                    "person_name":None,
                    "org_name":None,
                    "next_activity_subject":None,
                    "next_activity_type":None,
                    "next_activity_duration":None,
                    "next_activity_note":None,
                    "formatted_value":"0 $",
                    "rotten_time":None,
                    "weighted_value":0,
                    "formatted_weighted_value":"0 $",
                    "owner_name":"TEST_owner",
                    "cc_email":"mycompany+deal2@pipedrivemail.com",
                    "org_hidden":False,
                    "person_hidden":False
                },
            "indexable_fields":[],
            "event":"updated.deal"
        }

        response = c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Deal.objects.count(), 1)

        instance = Deal.objects.get(external_id=999)

        self.assertEquals(instance.value, 1000)

    def test_create_person(self):

        c = Client()

        self.assertEquals(Person.objects.count(), 0)

        data = {
              "v":1,
              "matches_filters":{"current":[],
              "previous":[]},
              "meta":
                {
                  "v":1,
                  "action":"added",
                  "object":"person",
                  "id":998,
                  "company_id":1689563,
                  "user_id":2428657,
                  "host":"miempresa2.pipedrive.com",
                  "timestamp":1492650227,
                  "timestamp_milli":1492650227536,
                  "permitted_user_ids":[2428657],
                  "trans_pending":False,
                  "is_bulk_update":False,
                  "elastic_enabled":True,
                  "matches_filters":{"current":[],
                  "previous":[]}
                },
              "retry":0,
              "current":
                {
                  "id":998,
                  "company_id":1689563,
                  "owner_id":2428657,
                  "org_id":None,
                  "name":"TEST_NAME",
                  "first_name":"TEST_LASTNAME",
                  "last_name":None,
                  "open_deals_count":0,
                  "related_open_deals_count":0,
                  "closed_deals_count":0,
                  "related_closed_deals_count":0,
                  "participant_open_deals_count":0,
                  "participant_closed_deals_count":0,
                  "email_messages_count":0,
                  "activities_count":0,
                  "done_activities_count":0,
                  "undone_activities_count":0,
                  "reference_activities_count":0,
                  "files_count":0,
                  "notes_count":0,
                  "followers_count":0,
                  "won_deals_count":0,
                  "related_won_deals_count":0,
                  "lost_deals_count":0,
                  "related_lost_deals_count":0,
                  "active_flag":True,
                  "phone":[
                    {"label":"work",
                    "value":"22222222",
                    "primary":True}],
                  "email":[
                    {"label":"work",
                    "value":"mail@example.com",
                    "primary":True}],
                  "first_char":"p",
                  "update_time":"2017-04-20 01:03:47",
                  "add_time":"2017-04-20 01:03:47",
                  "visible_to":"3",
                  "picture_id":None,
                  "next_activity_date":None,
                  "next_activity_time":None,
                  "next_activity_id":None,
                  "last_activity_id":None,
                  "last_activity_date":None,
                  "last_incoming_mail_time":None,
                  "last_outgoing_mail_time":None,
                  "org_name":None,
                  "cc_email":"miempresa2@pipedrivemail.com",
                  "owner_name":"Gustavo"
                },
              "previous":None,
              "indexable_fields":[],
              "event":"added.person"
            }

        response = c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Person.objects.count(), 1)

        instance = Person.objects.get(external_id=998)

        self.assertEquals(instance.name, "TEST_NAME")



class TestPipedriveCreation(TestCase):

    def test_create_organization(self):

        organization = Organization.objects.create(name="TEST_ORGANIZATION")

        result = organization.upload()

        self.assertTrue(result)
        self.assertIsNotNone(organization.external_id)

    def test_create_person(self):

        person = Person.objects.create(name="TEST_PERSON")

        result = person.upload()

        self.assertTrue(result)
        self.assertIsNotNone(person.external_id)

    def test_create_deal(self):

        deal = Deal.objects.create(title="TEST_DEAL")

        result = deal.upload()

        self.assertTrue(result)
        self.assertIsNotNone(deal.external_id)

class TestPipedrive(TestCase):

    def setUp(self):
        DealField.get_fields()
        OrganizationField.get_fields()
        PersonField.get_fields()
        Pipeline.get_fields()
        Stage.get_fields()

    def test_datetime_from_fields_none_fields(self):

        el = {
            "next_activity_date": None,
            "next_activity_time": None
        }

        result = Organization.datetime_from_fields(el, 'next_activity_date', 'next_activity_time')

        self.assertIsNone(result)

    def test_datetime_from_fields_empty_el(self):

        el = {}

        result = Organization.datetime_from_fields(el, 'next_activity_date', 'next_activity_time')

        self.assertIsNone(result)

    def test_datetime_from_fields_correct(self):

        el = {
            "next_activity_date": "2017-03-20",
            "next_activity_time": "14:01:02"
        }

        result = Organization.datetime_from_fields(el, 'next_activity_date', 'next_activity_time')
        expected = datetime.datetime(2017, 3, 20, 14, 1, 2, 0, tzinfo=pytz.utc)

        self.assertEquals(result, expected)

    def test_datetime_from_simple_time_correct(self):

        el = {u'update_time': u'2017-04-03 16:21:12'}

        result = Organization.datetime_from_simple_time(el, u'update_time')
        expected = datetime.datetime(2017, 4, 3, 16, 21, 12, 0, tzinfo=pytz.utc)

        self.assertEquals(result, expected)

    def test_datetime_from_simple_time_empty_el(self):

        el = {}

        result = Organization.datetime_from_simple_time(el, u'update_time')

        self.assertIsNone(result)

    def test_datetime_from_simple_time_none_field(self):

        el = {u'update_time': None}

        result = Organization.datetime_from_simple_time(el, u'update_time')

        self.assertIsNone(result)

    def test_get_primary_correct(self):

        el = {
            u'email':
                [
                    {u'primary': False,
                     u'value': u'example2@example.com',
                     u'label': u'work'},
                    {u'primary': True,
                     u'value': u'example@example.com',
                     u'label': u'work'}
                ]
        }

        result = Person.get_primary(el, u'email')
        expected = u'example@example.com'

        self.assertEquals(result, expected)

    def test_get_primary_none(self):

        el = {}

        result = Person.get_primary(el, u'email')

        self.assertIsNone(result)

    def test_fetch_from_pipedrive_organizations(self):

        result = Organization.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_persons(self):

        result = Person.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_deals(self):

        result = Deal.fetch_from_pipedrive()

        self.assertTrue(result)