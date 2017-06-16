# -*- coding: utf-8 -*-

# Create your tests here.

import pytz
import datetime
import json
import logging

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import Client

from pipedrive.models import Deal
from pipedrive.models import Person
from pipedrive.models import Organization
from pipedrive.models import PersonField
from pipedrive.models import DealField
from pipedrive.models import OrganizationField
from pipedrive.models import Pipeline
from pipedrive.models import Stage
from pipedrive.models import User
from pipedrive.models import Note
from pipedrive.models import Activity
from pipedrive.models import PipedriveModel
from pipedrive.models import FieldModification

from pipedrive.utils import compare_dicts


class TestPipedriveWebhooks(TestCase):

    def test_activity_marked_as_done(self):

        c = Client()

        Activity.objects.create(external_id=2)

        self.assertEquals(Activity.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []},
            "meta": {
                "v": 1,
                "action": "updated",
                "object": "activity",
                "id": 2,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "miempresa2.pipedrive.com",
                "timestamp": 1492898177,
                "timestamp_milli": 1492898177841,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 2,
                "company_id": 1689563,
                "user_id": 2428657,
                "done": True,
                "type": "call",
                "reference_type": "none",
                "reference_id": None,
                "due_date": "2017-04-21",
                "due_time": "",
                "duration": "",
                "add_time": "2017-04-21 12:21:10",
                "marked_as_done_time": "2017-04-22 21:56:17",
                "subject": "TEST_ACTIVITY",
                "deal_id": None,
                "org_id": None,
                "person_id": None,
                "active_flag": True,
                "update_time": "2017-04-22 21:56:17",
                "gcal_event_id": None,
                "google_calendar_id": None,
                "google_calendar_etag": None,
                "note": "",
                "person_name": None,
                "org_name": None,
                "deal_title": None,
                "assigned_to_user_id": 2428657,
                "created_by_user_id": 2428657,
                "owner_name": "Gustavo",
                "person_dropbox_bcc": None,
                "deal_dropbox_bcc": None,
                "no_gcal": False
            },
            "previous": {
                "id": 2,
                "company_id": 1689563,
                "user_id": 2428657,
                "done": False,
                "type": "call",
                "reference_type": "none",
                "reference_id": None,
                "due_date": "2017-04-21",
                "due_time": "",
                "duration": "",
                "add_time": "2017-04-21 12:21:10",
                "marked_as_done_time": "",
                "subject": "TEST_ACTIVITY",
                "deal_id": None,
                "org_id": None,
                "person_id": None,
                "active_flag": True,
                "update_time": "2017-04-22 21:56:15",
                "gcal_event_id": None,
                "google_calendar_id": None,
                "google_calendar_etag": None,
                "note": "",
                "person_name": None,
                "org_name": None,
                "deal_title": None,
                "assigned_to_user_id": 2428657,
                "created_by_user_id": 2428657,
                "owner_name": "Gustavo",
                "person_dropbox_bcc": None,
                "deal_dropbox_bcc": None
            },
            "event": "updated.activity"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        activity = Activity.objects.get(external_id=2)
        expected = datetime.datetime(2017, 4, 22, 21, 56, 17, tzinfo=pytz.utc)

        self.assertEquals(activity.marked_as_done_time, expected)

    def test_activity_not_marked_as_done(self):

        c = Client()

        Activity.objects.create(external_id=2)

        self.assertEquals(Activity.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []
            },
            "meta": {
                "v": 1,
                "action": "updated",
                "object": "activity",
                "id": 2,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "miempresa2.pipedrive.com",
                "timestamp": 1492898177,
                "timestamp_milli": 1492898177841,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 2,
                "company_id": 1689563,
                "user_id": 2428657,
                "done": True,
                "type": "call",
                "reference_type": "none",
                "reference_id": None,
                "due_date": "2017-04-21",
                "due_time": "",
                "duration": "",
                "add_time": "2017-04-21 12:21:10",
                "marked_as_done_time": "",
                "subject": "TEST_ACTIVITY",
                "deal_id": None,
                "org_id": None,
                "person_id": None,
                "active_flag": True,
                "update_time": "2017-04-22 21:56:17",
                "gcal_event_id": None,
                "google_calendar_id": None,
                "google_calendar_etag": None,
                "note": "",
                "person_name": None,
                "org_name": None,
                "deal_title": None,
                "assigned_to_user_id": 2428657,
                "created_by_user_id": 2428657,
                "owner_name": "Gustavo",
                "person_dropbox_bcc": None,
                "deal_dropbox_bcc": None,
                "no_gcal": False
            },
            "previous": {
                "id": 2,
                "company_id": 1689563,
                "user_id": 2428657,
                "done": False,
                "type": "call",
                "reference_type": "none",
                "reference_id": None,
                "due_date": "2017-04-21",
                "due_time": "",
                "duration": "",
                "add_time": "2017-04-21 12:21:10",
                "marked_as_done_time": "",
                "subject": "TEST_ACTIVITY",
                "deal_id": None,
                "org_id": None,
                "person_id": None,
                "active_flag": True,
                "update_time": "2017-04-22 21:56:15",
                "gcal_event_id": None,
                "google_calendar_id": None,
                "google_calendar_etag": None,
                "note": "",
                "person_name": None,
                "org_name": None,
                "deal_title": None,
                "assigned_to_user_id": 2428657,
                "created_by_user_id": 2428657,
                "owner_name": "Gustavo",
                "person_dropbox_bcc": None,
                "deal_dropbox_bcc": None
            },
            "event": "updated.activity"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        activity = Activity.objects.get(external_id=2)

        self.assertIsNone(activity.marked_as_done_time)

    def test_create_organization(self):

        c = Client()

        User.objects.create(external_id=123456)

        self.assertEquals(Stage.objects.count(), 0)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []
            },
            "meta": {
                "v": 1,
                "action": "added",
                "object": "organization",
                "id": 71,
                "company_id": 1689563,
                "user_id": 123456,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492893731,
                "timestamp_milli": 1492893731834,
                "permitted_user_ids": [123456, 1428742],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 71,
                "company_id": 666,
                "owner_id": 123456,
                "name": "The organization",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "email_messages_count": 0,
                "people_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 0,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "category_id": None,
                "picture_id": None,
                "country_code": None,
                "first_char": "l",
                "update_time": "2017-04-22 20:42:11",
                "add_time": "2017-04-22 20:42:11",
                "visible_to": "3",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "address": "Avenida Los Pajaritos 1500, Santiago, Chile",
                "address_lat": -33.5135078,
                "address_long": -70.7574387,
                "address_subpremise": "",
                "address_street_number": "1500",
                "address_route": "Avenida Los Pajaritos",
                "address_sublocality": "",
                "address_locality": "Maipú",
                "address_admin_area_level_1": "Región Metropolitana",
                "address_admin_area_level_2": "Santiago",
                "address_country": "Chile",
                "address_postal_code": "",
                "address_formatted_address": "Some address",
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "TEST_OWNER",
                "edit_name": True
            },
            "previous": None,
            "indexable_fields": [],
            "event": "added.organization"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Organization.objects.count(), 1)

        organization = Organization.objects.get(external_id=71)

        self.assertEquals(organization.name, "The organization")

    def test_update_deal(self):
        c = Client()

        Deal.objects.create(
            title="TEST_DEAL",
            external_id=999,
            value=0,
        )

        Pipeline.objects.create(external_id=1)

        self.assertEquals(Deal.objects.count(), 1)
        self.assertEquals(Pipeline.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters":
                {
                    "current": [],
                    "previous": []
                },
            "meta":
                {
                    "v": 1,
                    "action": "updated",
                    "object": "deal",
                    "id": 999,
                    "company_id": 1689563,
                    "user_id": 2428657,
                    "host": "mycompany.pipedrive.com",
                    "timestamp": 1492636837,
                    "timestamp_milli": 1492636837696,
                    "permitted_user_ids": [2428657],
                    "trans_pending": False,
                    "is_bulk_update": False,
                    "elastic_enabled": True,
                    "matches_filters": {
                        "current": [],
                        "previous": []
                    }
                },
            "retry": 0,
            "current":
                {
                    "id": 999,
                    "creator_user_id": 2428657,
                    "user_id": {
                        "id": 2428657,
                        "name": "SOME USER",
                        "email": "user@example.com",
                        "has_pic": False,
                        "pic_hash": None,
                        "active_flag": True,
                        "value": 1656137
                    },
                    "person_id": None,
                    "org_id": None,
                    "stage_id": 1,
                    "title": "TEST_DEAL",
                    "value": 1000,
                    "currency": "USD",
                    "add_time": "2017-04-19 19:43:40",
                    "update_time": "2017-04-19 21:20:37",
                    "stage_change_time": None,
                    "active": True,
                    "deleted": False,
                    "status": "open",
                    "next_activity_date": None,
                    "next_activity_time": None,
                    "next_activity_id": None,
                    "last_activity_id": None,
                    "last_activity_date": None,
                    "lost_reason": None,
                    "visible_to": "3",
                    "close_time": None,
                    "pipeline_id": 1,
                    "won_time": None,
                    "first_won_time": None,
                    "lost_time": None,
                    "products_count": 0,
                    "files_count": 0,
                    "notes_count": 0,
                    "followers_count": 1,
                    "email_messages_count": 0,
                    "activities_count": 0,
                    "done_activities_count": 0,
                    "undone_activities_count": 0,
                    "reference_activities_count": 0,
                    "participants_count": 0,
                    "expected_close_date": None,
                    "last_incoming_mail_time": None,
                    "last_outgoing_mail_time": None,
                    "stage_order_nr": 1,
                    "person_name": None,
                    "org_name": None,
                    "next_activity_subject": None,
                    "next_activity_type": None,
                    "next_activity_duration": None,
                    "next_activity_note": None,
                    "formatted_value": "1 000 $",
                    "rotten_time": None,
                    "weighted_value": 1000,
                    "formatted_weighted_value": "1 000 $",
                    "owner_name": "TEST_owner",
                    "cc_email": "mycompany+deal2@pipedrivemail.com",
                    "org_hidden": False,
                    "person_hidden": False
                },
            "previous":
                {
                    "id": 999,
                    "creator_user_id": 2428657,
                    "user_id": 2428657,
                    "person_id": None,
                    "org_id": None,
                    "stage_id": 1,
                    "title": "TEST_DEAL",
                    "value": 0,
                    "currency": "USD",
                    "add_time": "2017-04-19 19:43:40",
                    "update_time": "2017-04-19 19:43:41",
                    "stage_change_time": None,
                    "active": True,
                    "deleted": False,
                    "status": "open",
                    "next_activity_date": None,
                    "next_activity_time": None,
                    "next_activity_id": None,
                    "last_activity_id": None,
                    "last_activity_date": None,
                    "lost_reason": None,
                    "visible_to": "3",
                    "close_time": None,
                    "pipeline_id": 5,
                    "won_time": None,
                    "first_won_time": None,
                    "lost_time": None,
                    "products_count": 0,
                    "files_count": 0,
                    "notes_count": 0,
                    "followers_count": 1,
                    "email_messages_count": 0,
                    "activities_count": 0,
                    "done_activities_count": 0,
                    "undone_activities_count": 0,
                    "reference_activities_count": 0,
                    "participants_count": 0,
                    "expected_close_date": None,
                    "last_incoming_mail_time": None,
                    "last_outgoing_mail_time": None,
                    "stage_order_nr": 1,
                    "person_name": None,
                    "org_name": None,
                    "next_activity_subject": None,
                    "next_activity_type": None,
                    "next_activity_duration": None,
                    "next_activity_note": None,
                    "formatted_value": "0 $",
                    "rotten_time": None,
                    "weighted_value": 0,
                    "formatted_weighted_value": "0 $",
                    "owner_name": "TEST_owner",
                    "cc_email": "mycompany+deal2@pipedrivemail.com",
                    "org_hidden": False,
                    "person_hidden": False
                },
            "indexable_fields": [],
            "event": "updated.deal"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Deal.objects.count(), 1)

        instance = Deal.objects.get(external_id=999)

        self.assertEquals(instance.value, 1000)

        self.assertEquals(instance.pipeline.external_id, 1)

    def test_update_pipeline(self):

        c = Client()

        Pipeline.objects.create(external_id=1, name="EXAMPLE_PIPELINE")

        self.assertEquals(Pipeline.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": None,
            "meta": {
                "v": 1,
                "action": "updated",
                "object": "pipeline",
                "id": "1",
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492704744,
                "timestamp_milli": 1492704744018,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False
            },
            "retry": 0,
            "current": {
                "id": 1,
                "name": "EXAMPLE_PIPELINE_2",
                "url_title": "ThatPipeline",
                "order_nr": 1,
                "active": True,
                "add_time": "2017-04-13 16:58:30",
                "update_time": "2017-04-20 16:12:23"
            },
            "previous": {
                "id": 1,
                "name": "EXAMPLE_PIPELINE",
                "url_title": "default",
                "order_nr": 1,
                "active": True,
                "add_time": "2017-04-13 16:58:30",
                "update_time": None
            },
            "event": "updated.pipeline"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Pipeline.objects.count(), 1)

        pipeline = Pipeline.objects.get(external_id=1)

        self.assertEquals(pipeline.name, "EXAMPLE_PIPELINE_2")

    def test_create_person(self):

        c = Client()

        self.assertEquals(Person.objects.count(), 0)

        User.objects.create(external_id=111)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []},
            "meta": {
                "v": 1,
                "action": "added",
                "object": "person",
                "id": 998,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492650227,
                "timestamp_milli": 1492650227536,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True,
                "matches_filters":
                {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 998,
                "company_id": 1689563,
                "owner_id": 111,
                "org_id": None,
                "name": "TEST_NAME",
                "first_name": "TEST_LASTNAME",
                "last_name": None,
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "participant_open_deals_count": 0,
                "participant_closed_deals_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 0,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "phone": [
                    {
                        "label": "work",
                        "value": "22222222",
                        "primary": True
                    }
                ],
                "email": [
                    {
                        "label": "work",
                        "value": "mail@example.com",
                        "primary": True
                    }
                ],
                "first_char": "p",
                "update_time": "2017-04-20 01:03:47",
                "add_time": "2017-04-20 01:03:47",
                "visible_to": "3",
                "picture_id": None,
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "org_name": None,
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "OWNER"
            },
            "previous": None,
            "indexable_fields": [],
            "event": "added.person"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Person.objects.count(), 1)

        instance = Person.objects.get(external_id=998)

        self.assertEquals(instance.name, "TEST_NAME")

        self.assertEquals(instance.owner.external_id, 111)

    def test_create_person_unicode(self):

        c = Client()

        self.assertEquals(Person.objects.count(), 0)

        User.objects.create(external_id=111)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []},
            "meta": {
                "v": 1,
                "action": "added",
                "object": "person",
                "id": 998,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492650227,
                "timestamp_milli": 1492650227536,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True,
                "matches_filters":
                {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 998,
                "company_id": 1689563,
                "owner_id": 111,
                "org_id": None,
                "name": u"हुएआदि विश्वास परि",
                "first_name": u"प्राथमिक जैसे जानते",
                "last_name": None,
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "participant_open_deals_count": 0,
                "participant_closed_deals_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 0,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "phone": [
                    {
                        "label": "work",
                        "value": "22222222",
                        "primary": True
                    }
                ],
                "email": [
                    {
                        "label": "work",
                        "value": "mail@example.com",
                        "primary": True
                    }
                ],
                "first_char": "p",
                "update_time": "2017-04-20 01:03:47",
                "add_time": "2017-04-20 01:03:47",
                "visible_to": "3",
                "picture_id": None,
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "org_name": None,
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "OWNER"
            },
            "previous": None,
            "indexable_fields": [],
            "event": "added.person"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Person.objects.count(), 1)

        instance = Person.objects.get(external_id=998)

        self.assertEquals(instance.name, u"हुएआदि विश्वास परि")

        self.assertEquals(instance.owner.external_id, 111)

    def test_create_activity(self):

        c = Client()

        self.assertEquals(Activity.objects.count(), 0)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []
            },
            "meta": {
                "v": 1,
                "action": "added",
                "object": "activity",
                "id": 1,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492700133,
                "timestamp_milli": 1492700133328,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 1,
                "company_id": 1689563,
                "user_id": 2428657,
                "done": False,
                "type": "call",
                "reference_type": "none",
                "reference_id": None,
                "due_date": "2017-04-20",
                "due_time": "16:00",
                "duration": "01:30",
                "add_time": "2017-04-20 14:55:33",
                "marked_as_done_time": "",
                "subject": "That call",
                "deal_id": 14,
                "org_id": 18,
                "person_id": 6,
                "active_flag": True,
                "update_time": "2017-04-20 14:55:33",
                "gcal_event_id": None,
                "google_calendar_id": None,
                "google_calendar_etag": None,
                "note": "It is an important call",
                "person_name": "TEST_PERSON",
                "org_name": "TEST_ORGANIZATION",
                "deal_title": "TEST_DEAL",
                "assigned_to_user_id": 2428657,
                "created_by_user_id": 2428657,
                "owner_name": "TEST_OWNER",
                "person_dropbox_bcc": "mycompany@pipedrivemail.com",
                "deal_dropbox_bcc": "mycompany+deal14@pipedrivemail.com",
                "updates_story_id": 69,
                "no_gcal": False
            },
            "previous": None,
            "event": "added.activity"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Activity.objects.count(), 1)

        activity = Activity.objects.get(external_id=1)

        self.assertEquals(activity.type, "call")
        self.assertEquals(activity.subject, "That call")

    def test_create_person_in_organization(self):

        c = Client()

        self.assertEquals(Person.objects.count(), 0)

        Organization.objects.create(external_id=992)

        self.assertEquals(Organization.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []},
            "meta": {
                "v": 1,
                "action": "added",
                "object": "person",
                "id": 998,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492650227,
                "timestamp_milli": 1492650227536,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True,
                "matches_filters":
                {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 998,
                "company_id": 1689563,
                "owner_id": 2428657,
                "org_id": 992,
                "name": "TEST_NAME",
                "first_name": "TEST_LASTNAME",
                "last_name": None,
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "participant_open_deals_count": 0,
                "participant_closed_deals_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 0,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "phone": [
                    {
                        "label": "work",
                        "value": "22222222",
                        "primary": True
                    }
                ],
                "email": [
                    {
                        "label": "work",
                        "value": "mail@example.com",
                        "primary": True
                    }
                ],
                "first_char": "p",
                "update_time": "2017-04-20 01:03:47",
                "add_time": "2017-04-20 01:03:47",
                "visible_to": "3",
                "picture_id": None,
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "org_name": None,
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "OWNER"
            },
            "previous": None,
            "indexable_fields": [],
            "event": "added.person"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Person.objects.count(), 1)

        person = Person.objects.get(external_id=998)

        self.assertEquals(person.name, "TEST_NAME")

        organization = Organization.objects.get(external_id=992)

        self.assertEquals(organization.person_set.count(), 1)

    def test_create_stage(self):

        c = Client()

        self.assertEquals(Stage.objects.count(), 0)

        data = {
            "v": 1,
            "matches_filters": None,
            "meta": {
                "v": 1,
                "action": "added",
                "object": "stage",
                "id": 6,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492712041,
                "timestamp_milli": 1492712041663,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False
            },
            "retry": 0,
            "current": {
                "id": 6,
                "order_nr": 6,
                "name": "TEST_STAGE",
                "active_flag": True,
                "deal_probability": 100,
                "pipeline_id": 1,
                "rotten_flag": True,
                "rotten_days": 5,
                "add_time": "2017-04-20 18:14:01",
                "update_time": "2017-04-20 18:14:01"
            },
            "previous": None,
            "event": "added.stage"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Stage.objects.count(), 1)

        stage = Stage.objects.get(external_id=6)

        self.assertEquals(stage.name, "TEST_STAGE")

    def test_delete_organization(self):

        c = Client()

        Organization.objects.create(
            name="TEST_ORGANIZATION",
            external_id=997,
        )

        self.assertEquals(Organization.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters":
            {
                "current": [],
                "previous": []
            },
            "meta":
            {
                "v": 1,
                "action": "deleted",
                "object": "organization",
                "id": 997,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492653308,
                "timestamp_milli": 1492653308072,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True,
                "matches_filters":
                {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": None,
            "previous":
            {
                "id": 997,
                "company_id": 1689563,
                "owner_id": 2428657,
                "name": "TEST_ORGANIZATION",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "email_messages_count": 0,
                "people_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "category_id": None,
                "picture_id": None,
                "country_code": None,
                "first_char": "t",
                "update_time": "2017-04-19 19:43:41",
                "add_time": "2017-04-19 19:43:41",
                "visible_to": "3",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "address": None,
                "address_lat": None,
                "address_long": None,
                "address_subpremise": None,
                "address_street_number": None,
                "address_route": None,
                "address_sublocality": None,
                "address_locality": None,
                "address_admin_area_level_1": None,
                "address_admin_area_level_2": None,
                "address_country": None,
                "address_postal_code": None,
                "address_formatted_address": None,
                "owner_name": "OWNER",
                "cc_email": "mycompany@pipedrivemail.com"
            },
            "indexable_fields": [],
            "event": "deleted.organization"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Organization.objects.count(), 1)
        self.assertEquals(Organization.objects.filter(deleted=True).count(), 1)

    def test_delete_inexistent_organization(self):

        c = Client()

        self.assertEquals(Organization.objects.count(), 0)
        User.objects.create(external_id=2428657)
        data = {
            "v": 1,
            "matches_filters":
            {
                "current": [],
                "previous": []
            },
            "meta":
            {
                "v": 1,
                "action": "deleted",
                "object": "organization",
                "id": 997,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492653308,
                "timestamp_milli": 1492653308072,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True,
                "matches_filters":
                {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": None,
            "previous":
            {
                "id": 997,
                "company_id": 1689563,
                "owner_id": 2428657,
                "name": "TEST_ORGANIZATION",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "email_messages_count": 0,
                "people_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "category_id": None,
                "picture_id": None,
                "country_code": None,
                "first_char": "t",
                "update_time": "2017-04-19 19:43:41",
                "add_time": "2017-04-19 19:43:41",
                "visible_to": "3",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "address": None,
                "address_lat": None,
                "address_long": None,
                "address_subpremise": None,
                "address_street_number": None,
                "address_route": None,
                "address_sublocality": None,
                "address_locality": None,
                "address_admin_area_level_1": None,
                "address_admin_area_level_2": None,
                "address_country": None,
                "address_postal_code": None,
                "address_formatted_address": None,
                "owner_name": "OWNER",
                "cc_email": "mycompany@pipedrivemail.com"
            },
            "indexable_fields": [],
            "event": "deleted.organization"
        }

        class fake_organization_api():
            def get_instances(self, **kwargs):
                return {
                    "success": True,
                    'data': [data['previous']],
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

            def get_instance(self, *args, **kwargs):
                return {
                    "success": True,
                    'data': data['previous'],
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

        old_org_api = Organization.pipedrive_api_client

        try:
            Organization.pipedrive_api_client = fake_organization_api()
            c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

            self.assertEquals(Organization.objects.count(), 1)
            self.assertEquals(Organization.objects.filter(deleted=True).count(), 1)

        finally:
            Organization.pipedrive_api_client = old_org_api

    def test_field_modification_when_delete_organization(self):

        c = Client()

        Organization.objects.create(
            name="TEST_ORGANIZATION",
            external_id=997,
        )

        self.assertEquals(FieldModification.objects.count(), 0)

        data = {
            "v": 1,
            "matches_filters":
            {
                "current": [],
                "previous": []
            },
            "meta":
            {
                "v": 1,
                "action": "deleted",
                "object": "organization",
                "id": 997,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492653308,
                "timestamp_milli": 1492653308072,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True,
                "matches_filters":
                {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": None,
            "previous":
            {
                "id": 997,
                "company_id": 1689563,
                "owner_id": 2428657,
                "name": "TEST_ORGANIZATION",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "email_messages_count": 0,
                "people_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "category_id": None,
                "picture_id": None,
                "country_code": None,
                "first_char": "t",
                "update_time": "2017-04-19 19:43:41",
                "add_time": "2017-04-19 19:43:41",
                "visible_to": "3",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "address": None,
                "address_lat": None,
                "address_long": None,
                "address_subpremise": None,
                "address_street_number": None,
                "address_route": None,
                "address_sublocality": None,
                "address_locality": None,
                "address_admin_area_level_1": None,
                "address_admin_area_level_2": None,
                "address_country": None,
                "address_postal_code": None,
                "address_formatted_address": None,
                "owner_name": "OWNER",
                "cc_email": "mycompany@pipedrivemail.com"
            },
            "indexable_fields": [],
            "event": "deleted.organization"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(FieldModification.objects.count(), 0)

    def test_merge_organizations(self):

        c = Client()

        Organization.objects.create(
            name="TEST_ORGANIZATION_1",
            external_id=996,
            owner_id=111
        )

        Organization.objects.create(
            name="TEST_ORGANIZATION_2",
            external_id=995,
        )

        User.objects.create(external_id=111)

        self.assertEquals(Organization.objects.count(), 2)

        data = {
            "v": 1,
            "matches_filters":
            {
                "current": [],
                "previous": []
            },
            "meta":
            {
                "v": 1,
                "action": "merged",
                "object": "organization",
                "id": 996,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492654463,
                "timestamp_milli": 1492654463572,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current":
            {
                "id": 996,
                "company_id": 1689563,
                "owner_id": 111,
                "name": "TEST_ORGANIZATION_1",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "email_messages_count": 0,
                "people_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "category_id": None,
                "picture_id": None,
                "country_code": None,
                "first_char": "t",
                "update_time": "2017-04-20 02:09:09",
                "add_time": "2017-04-19 19:42:27",
                "visible_to": "3",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "address": "d asda sd 3 r1",
                "address_lat": 52.8761635,
                "address_long": -1.493958,
                "address_subpremise": None,
                "address_street_number": "14",
                "address_route": "Arleston Lane",
                "address_sublocality": None,
                "address_locality": "Sinfin District Centre",
                "address_admin_area_level_1": "England",
                "address_admin_area_level_2": "Derby",
                "address_country": "Reino Unido",
                "address_postal_code": "DE24 3DS",
                "address_formatted_address": "Sinfin Shopping Centre-, Reino Unido",
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "OWNER",
                "edit_name": True,
                "merge_what_id": 995
            },
            "previous":
            {
                "id": 995,
                "company_id": 1689563,
                "owner_id": 222,
                "name": "TEST_ORGANIZATION_2",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "email_messages_count": 0,
                "people_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "category_id": None,
                "picture_id": None,
                "country_code": None,
                "first_char": "t",
                "update_time": "2017-04-20 02:09:09",
                "add_time": "2017-04-19 19:42:27",
                "visible_to": "3",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "address": "d asda sd 3 r1",
                "address_lat": 52.8761635,
                "address_long": -1.493958,
                "address_subpremise": None,
                "address_street_number": "14",
                "address_route": "Arleston Lane",
                "address_sublocality": None,
                "address_locality": "Sinfin District Centre",
                "address_admin_area_level_1": "England",
                "address_admin_area_level_2": "Derby",
                "address_country": "Reino Unido",
                "address_postal_code": "DE24 3DS",
                "address_formatted_address": "Sinfin Shopping Centre, Reino Unido",
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "OWNER",
                "edit_name": True
            },
            "event": "merged.organization"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Organization.objects.count(), 2)

        organization = Organization.objects.get(external_id=996)

        self.assertEquals(organization.owner.external_id, 111)

    def test_create_person_note(self):

        c = Client()

        data = {
            "v": 1,
            "matches_filters": None,
            "meta":
            {
                "v": 1,
                "action": "added",
                "object": "note",
                "id": 995,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492687681,
                "timestamp_milli": 1492687681417,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True
            },
            "retry": 0,
            "current": {
                "id": 995,
                "user_id": 2428657,
                "deal_id": None,
                "person_id": 994,
                "org_id": None,
                "content": "This is an example note",
                "add_time": "2017-04-20 11:28:01",
                "update_time": "2017-04-20 11:28:01",
                "active_flag": True,
                "pinned_to_deal_flag": False,
                "pinned_to_person_flag": False,
                "pinned_to_organization_flag": False,
                "last_update_user_id": None,
                "organization": None,
                "person": {"name": "TEST_PERSON"},
                "deal": None,
                "user": {
                    "email": "user@example.com",
                    "name": "TEST_USER",
                    "icon_url": None,
                    "is_you": True
                }
            },
            "previous": None,
            "event": "added.note"
        }

        Person.objects.create(external_id=994)

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Note.objects.count(), 1)

        note = Note.objects.get(external_id=995)

        self.assertEquals(note.content, "This is an example note")

        person = Person.objects.get(external_id=994)

        self.assertEquals(person.note_set.count(), 1)

    def test_create_organization_note(self):

        c = Client()

        data = {
            "v": 1,
            "matches_filters": None,
            "meta":
            {
                "v": 1,
                "action": "added",
                "object": "note",
                "id": 995,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492687681,
                "timestamp_milli": 1492687681417,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True
            },
            "retry": 0,
            "current": {
                "id": 995,
                "user_id": 2428657,
                "deal_id": None,
                "person_id": None,
                "org_id": 993,
                "content": "This is an example note",
                "add_time": "2017-04-20 11:28:01",
                "update_time": "2017-04-20 11:28:01",
                "active_flag": True,
                "pinned_to_deal_flag": False,
                "pinned_to_person_flag": False,
                "pinned_to_organization_flag": False,
                "last_update_user_id": None,
                "organization": None,
                "person": {"name": "TEST_PERSON"},
                "deal": None,
                "user": {
                    "email": "user@example.com",
                    "name": "TEST_USER",
                    "icon_url": None,
                    "is_you": True
                }
            },
            "previous": None,
            "event": "added.note"
        }

        Organization.objects.create(external_id=993)

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Note.objects.count(), 1)

        note = Note.objects.get(external_id=995)

        self.assertEquals(note.content, "This is an example note")

        organization = Organization.objects.get(external_id=993)

        self.assertEquals(organization.note_set.count(), 1)

    def test_create_deal_note(self):

        c = Client()

        data = {
            "v": 1,
            "matches_filters": None,
            "meta": {
                "v": 1,
                "action": "added",
                "object": "note",
                "id": 995,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492687681,
                "timestamp_milli": 1492687681417,
                "permitted_user_ids": ["*"],
                "trans_pending": False,
                "is_bulk_update": False,
                "elastic_enabled": True
            },
            "retry": 0,
            "current": {
                "id": 995,
                "user_id": 2428657,
                "deal_id": 992,
                "person_id": None,
                "org_id": None,
                "content": "This is an example note",
                "add_time": "2017-04-20 11:28:01",
                "update_time": "2017-04-20 11:28:01",
                "active_flag": True,
                "pinned_to_deal_flag": False,
                "pinned_to_person_flag": False,
                "pinned_to_organization_flag": False,
                "last_update_user_id": None,
                "organization": None,
                "person": {"name": "TEST_PERSON"},
                "deal": None,
                "user": {
                    "email": "user@example.com",
                    "name": "TEST_USER",
                    "icon_url": None,
                    "is_you": True
                }
            },
            "previous": None,
            "event": "added.note"
        }

        Deal.objects.create(external_id=992)

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Note.objects.count(), 1)

        note = Note.objects.get(external_id=995)

        self.assertEquals(note.content, "This is an example note")

        deal = Deal.objects.get(external_id=992)

        self.assertEquals(deal.note_set.count(), 1)

    def test_create_deal_with_organization(self):

        c = Client()

        Person.objects.create(external_id=5)
        Organization.objects.create(external_id=18)

        self.assertEquals(Person.objects.count(), 1)
        self.assertEquals(Organization.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []
            },
            "meta": {
                "v": 1,
                "action": "added",
                "object": "deal",
                "id": 9,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492695625,
                "timestamp_milli": 1492695625650,
                "permitted_user_ids": [2428657],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 9,
                "creator_user_id": 2428657,
                "user_id": 2428657,
                "person_id": 5,
                "org_id": 18,
                "stage_id": 1,
                "title": "TEST_ORGANIZATION negocio",
                "value": 3500,
                "currency": "CLF",
                "add_time": "2017-04-20 13:40:25",
                "update_time": "2017-04-20 13:40:25",
                "stage_change_time": None,
                "active": True,
                "deleted": False,
                "status": "open",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "lost_reason": None,
                "visible_to": "3",
                "close_time": None,
                "pipeline_id": 1,
                "won_time": None,
                "first_won_time": None,
                "lost_time": None,
                "products_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "participants_count": 0,
                "expected_close_date": "2017-04-29",
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "stage_order_nr": 1,
                "person_name": "TEST_PERSON",
                "org_name": "TEST_ORGANIZATION",
                "next_activity_subject": None,
                "next_activity_type": None,
                "next_activity_duration": None,
                "next_activity_note": None,
                "formatted_value": "3 500 CLF",
                "rotten_time": None,
                "weighted_value": 3500,
                "formatted_weighted_value": "3 500 CLF",
                "owner_name": "TEST_USER",
                "cc_email": "mycompany+deal9@pipedrivemail.com",
                "org_hidden": False,
                "person_hidden": False
            },
            "previous": None,
            "indexable_fields": [],
            "event": "added.deal"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        deal = Deal.objects.get(external_id=9)

        self.assertEquals(deal.person.external_id, 5)
        self.assertEquals(deal.org.external_id, 18)

    def test_create_person_with_additional_fields(self):

        c = Client()

        Person.objects.create(external_id=84)

        self.assertEquals(Person.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []
            },
            "meta": {
                "v": 1,
                "action": "added",
                "object": "person",
                "id": 84,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "mycompany.pipedrive.com",
                "timestamp": 1492990137,
                "timestamp_milli": 1492990137771,
                "permitted_user_ids": [2428657, 1428742],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 84,
                "company_id": 1689563,
                "owner_id": 2428657,
                "org_id": None,
                "name": "NEW PERSON",
                "first_name": "NEW",
                "last_name": "PERSON",
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "participant_open_deals_count": 0,
                "participant_closed_deals_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 0,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "phone": [{
                    "label": "work",
                    "value": "3232635+6",
                    "primary": True
                }],
                "email": [{
                    "label": "work",
                    "value": "address@example.com",
                    "primary": True
                }],
                "first_char": "n",
                "update_time": "2017-04-23 23:28:57",
                "add_time": "2017-04-23 23:28:57",
                "visible_to": "3",
                "picture_id": None,
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "66fb3447cad79ece76413df362fea1122856bcb3": 45,
                "org_name": None,
                "cc_email": "mycompany@pipedrivemail.com",
                "owner_name": "OWNER"
            },
            "previous": None,
            "indexable_fields": ["66fb3447cad79ece76413df362fea1122856bcb3"],
            "event": "added.person"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        person = Person.objects.get(external_id=84)

        additional_field = '66fb3447cad79ece76413df362fea1122856bcb3'

        self.assertEquals(person.additional_fields[additional_field], u'45')

    def test_update_person_with_additional_fields(self):

        c = Client()

        Person.objects.create(external_id=15)

        self.assertEquals(Person.objects.count(), 1)

        data = {
            "v": 1,
            "matches_filters": {
                "current": [],
                "previous": []
            },
            "meta": {
                "v": 1,
                "action": "updated",
                "object": "person",
                "id": 15,
                "company_id": 1689563,
                "user_id": 2428657,
                "host": "miempresa2.pipedrive.com",
                "timestamp": 1492987381,
                "timestamp_milli": 1492987381773,
                "permitted_user_ids": [2428657, 1428742],
                "trans_pending": False,
                "is_bulk_update": False,
                "matches_filters": {
                    "current": [],
                    "previous": []
                }
            },
            "retry": 0,
            "current": {
                "id": 15,
                "company_id": 1689563,
                "owner_id": 2428657,
                "org_id": None,
                "name": "TEST_PERSON",
                "first_name": "TEST_PERSON",
                "last_name": None,
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "participant_open_deals_count": 0,
                "participant_closed_deals_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "phone": [{
                    "label": "work",
                    "value": "3242342",
                    "primary": True
                }],
                "email": [{
                    "label": "work",
                    "value": "234234",
                    "primary": True
                }],
                "first_char": "t",
                "update_time": "2017-04-23 22:43:01",
                "add_time": "2017-04-20 14:42:48",
                "visible_to": "3",
                "picture_id": None,
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "66fb3447cad79ece76413df362fea1122856bcb3": 123,
                "org_name": None,
                "cc_email": "miempresa2@pipedrivemail.com"
            },
            "previous": {
                "id": 15,
                "company_id": 1689563,
                "owner_id": 2428657,
                "org_id": None,
                "name": "TEST_PERSON",
                "first_name": "TEST_PERSON",
                "last_name": None,
                "open_deals_count": 0,
                "related_open_deals_count": 0,
                "closed_deals_count": 0,
                "related_closed_deals_count": 0,
                "participant_open_deals_count": 0,
                "participant_closed_deals_count": 0,
                "email_messages_count": 0,
                "activities_count": 0,
                "done_activities_count": 0,
                "undone_activities_count": 0,
                "reference_activities_count": 0,
                "files_count": 0,
                "notes_count": 0,
                "followers_count": 1,
                "won_deals_count": 0,
                "related_won_deals_count": 0,
                "lost_deals_count": 0,
                "related_lost_deals_count": 0,
                "active_flag": True,
                "phone": [{
                    "value": "",
                    "primary": True
                }],
                "email": [{
                    "value": "",
                    "primary": True
                }],
                "first_char": "t",
                "update_time": "2017-04-20 14:42:48",
                "add_time": "2017-04-20 14:42:48",
                "visible_to": "3",
                "picture_id": None,
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "66fb3447cad79ece76413df362fea1122856bcb3": None,
                "org_name": None,
                "cc_email": "miempresa2@pipedrivemail.com"
            },
            "indexable_fields": ["66fb3447cad79ece76413df362fea1122856bcb3"],
            "event": "updated.person"
        }

        c.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        person = Person.objects.get(external_id=15)

        additional_field = '66fb3447cad79ece76413df362fea1122856bcb3'

        self.assertEquals(person.additional_fields[additional_field], u'123')


class TestPipedriveCreation(TestCase):

    def setUp(self):
        Pipeline.fetch_from_pipedrive()
        self.pipeline = Pipeline.objects.first()
        self.for_delete = []

    def tearDown(self):
        for instance in self.for_delete:
            instance.delete_from_pipedrive()

    def test_create_organization(self):

        organization = Organization.objects.create(name="TEST_ORGANIZATION")

        result = organization.upload()

        self.assertTrue(result)
        self.assertIsNotNone(organization.external_id)

        self.for_delete.append(organization)

    def test_upload_organization_with_id_at_additional_attributes(self):

        organization = Organization.objects.create(
            name="TEST_ORGANIZATION",
            additional_fields={'id': '3'}
        )

        result = organization.upload()

        self.assertTrue(result)
        self.assertIsNotNone(organization.external_id)

        self.for_delete.append(organization)

    def test_create_person(self):

        person = Person.objects.create(name="TEST_PERSON")

        result = person.upload()

        self.assertTrue(result)
        self.assertIsNotNone(person.external_id)

        self.for_delete.append(person)

    def test_create_deal(self):

        deal = Deal.objects.create(
            title="TEST_DEAL",
            pipeline_id=self.pipeline.external_id,
        )

        result = deal.upload()

        self.assertTrue(result)
        self.assertIsNotNone(deal.external_id)

        self.for_delete.append(deal)

    def test_create_deal_with_person(self):

        person = Person.objects.create(name="TEST_PERSON")
        person.upload()
        deal = Deal.objects.create(
            title="TEST_DEAL",
            person_id=person.external_id,
            pipeline_id=self.pipeline.external_id,
        )

        result = deal.upload()

        self.assertTrue(result)
        self.assertIsNotNone(deal.external_id)

        deal, created = Deal.sync_one(deal.external_id)

        self.assertFalse(created)
        self.assertEquals(deal.person_id, person.external_id)

        self.for_delete.append(deal)

    def test_create_person_with_organization(self):

        organization = Organization.objects.create(name="TEST_ORGANIZATION")
        organization.upload()
        person = Person.objects.create(
            name="TEST_PERSON",
            org_id=organization.external_id,
        )

        result = person.upload()

        self.assertTrue(result)
        self.assertIsNotNone(person.external_id)

        person, created = Person.sync_one(person.external_id)

        self.assertFalse(created)
        self.assertEquals(person.org_id, organization.external_id)

        self.for_delete.append(organization)
        self.for_delete.append(person)

    def test_create_stage(self):

        Pipeline.objects.create(
            name="TEST_PIPELINE",
            external_id=888,
        )

        stage = Stage.objects.create(name="TEST_STAGE", pipeline_id=888)

        self.assertEquals(stage.pipeline_id, 888)

        result = stage.upload()

        self.assertTrue(result)
        self.assertIsNotNone(stage.external_id)

        self.for_delete.append(stage)

    # def test_create_user(self):

    #     user = User.objects.create(name="TEST_USER", email="example@example.com")

    #     result = user.upload()

    #     self.assertTrue(result)
    #     self.assertIsNotNone(user.external_id)

    def test_create_pipeline(self):

        pipeline = Pipeline.objects.create(name="TEST_PIPELINE")

        result = pipeline.upload()

        self.assertTrue(result)
        self.assertIsNotNone(pipeline.external_id)

        self.for_delete.append(pipeline)

    def test_create_note(self):

        organization = Organization.objects.create(name="TEST_ORGANIZATION")

        result = organization.upload()

        self.assertIsNotNone(organization.external_id)

        note = Note.objects.create(content="TEST_NOTE", org_id=organization.external_id)

        result = note.upload()

        self.assertTrue(result)
        self.assertIsNotNone(note.external_id)

        self.for_delete.append(organization)
        self.for_delete.append(note)

    def test_create_activity(self):

        activity = Activity.objects.create(subject="TEST_ACTIVITY")

        result = activity.upload()

        self.assertTrue(result)
        self.assertIsNotNone(activity.external_id)

        self.for_delete.append(activity)

    def test_create_deal_field(self):

        deal_field = DealField.objects.create(
            name="TEST_DEAL_FIELD",
            field_type="text",
        )

        result = deal_field.upload()

        self.assertTrue(result)
        self.assertIsNotNone(deal_field.external_id)
        self.assertIsNotNone(deal_field.field_type)
        self.assertNotEquals(deal_field.key, u'')

        self.for_delete.append(deal_field)

    def test_create_person_field(self):

        person_field = PersonField.objects.create(
            name="TEST_PERSON_FIELD",
            field_type="text",
        )

        result = person_field.upload()

        self.assertTrue(result)
        self.assertIsNotNone(person_field.external_id)
        self.assertIsNotNone(person_field.field_type)
        self.assertNotEquals(person_field.key, u'')

        self.for_delete.append(person_field)

    def test_create_organization_field(self):

        organization_field = OrganizationField.objects.create(
            name="TEST_ORGANIZATION_FIELD",
            field_type="text",
        )

        result = organization_field.upload()

        self.assertTrue(result)
        self.assertIsNotNone(organization_field.external_id)
        self.assertIsNotNone(organization_field.field_type)
        self.assertNotEquals(organization_field.key, u'')

        self.for_delete.append(organization_field)


class TestCreateSyncAndUpload(TestCase):

    def case_create_sync_and_upload_instance(self, cls, field_name, defaults={}):
        """
        The test case creates a local instance, then it uploads it.
        After, it retrieves the instance from the API to change @field_name
        and upload it again.
        Finally the instance is retreived again to check that attributes were
        changed accordingly.
        """
        kwargs = {}
        kwargs[field_name] = "TEST_FIELD_1"
        kwargs.update(defaults)

        instance = cls.objects.create(**kwargs)

        result = instance.upload()

        self.assertTrue(result)
        self.assertIsNotNone(instance.external_id)
        self.assertEquals(getattr(instance, field_name), "TEST_FIELD_1")

        external_id = instance.external_id

        instance, created = cls.sync_one(external_id)

        self.assertEquals(getattr(instance, field_name), "TEST_FIELD_1")

        setattr(instance, field_name, "TEST_FIELD_2")
        for key in defaults.iterkeys():
            setattr(instance, key, defaults[key])

        result = instance.upload()

        self.assertTrue(result)

        instance, created = cls.sync_one(external_id)

        self.assertEquals(getattr(instance, field_name), "TEST_FIELD_2")

    def test_case_create_sync_and_upload_organization(self):

        self.case_create_sync_and_upload_instance(Organization, 'name')

    def test_case_create_sync_and_upload_person(self):

        self.case_create_sync_and_upload_instance(Person, 'name')

    def test_case_create_sync_and_upload_pipeline(self):

        self.case_create_sync_and_upload_instance(Pipeline, 'name')

    def test_case_create_sync_and_upload_organization_field(self):

        self.case_create_sync_and_upload_instance(
            OrganizationField, 'name', {'field_type': 'text'})

    def test_case_create_sync_and_upload_deal_deal(self):

        self.case_create_sync_and_upload_instance(DealField, 'name', {'field_type': 'text'})

    def test_case_create_sync_and_upload_person_field(self):

        self.case_create_sync_and_upload_instance(PersonField, 'name', {'field_type': 'text'})

    def test_case_create_sync_and_upload_activity(self):

        self.case_create_sync_and_upload_instance(Activity, 'subject')


class TestPipedriveCreationWithAdditionalFields(TestCase):

    def setUp(self):
        Pipeline.fetch_from_pipedrive()

        self.pipeline = Pipeline.objects.first()

    def test_create_organization_with_additional_fields(self):

        organization_field = OrganizationField.objects.create(
            name="TEST_ORGANIZATION_FIELD",
            field_type="text",
        )

        result = organization_field.upload()

        organization_kwargs = {}
        organization_kwargs['name'] = "TEST_ORGANIZATION"
        additional_fields = {}
        additional_fields[organization_field.key] = "TEST_TEXT"
        organization_kwargs['additional_fields'] = additional_fields

        organization = Organization.objects.create(**organization_kwargs)

        result = organization.upload()

        # The information appears locally
        self.assertTrue(result)
        self.assertIsNotNone(organization.external_id)
        self.assertIsNotNone(organization.name)
        self.assertIsNotNone(organization.additional_fields)
        self.assertIsNotNone(organization.additional_fields[organization_field.key])
        self.assertEquals(organization.additional_fields[organization_field.key], "TEST_TEXT")

        pipedrive_api_client = Organization.pipedrive_api_client

        online_organization = pipedrive_api_client.get_instance(organization.external_id)

        # The information appears online
        self.assertIsNotNone(online_organization[u'data'])
        self.assertEquals(online_organization[u'data'][u'name'], u"TEST_ORGANIZATION")
        self.assertTrue(organization_field.key in online_organization[u'data'])
        self.assertEquals(online_organization[u'data'][organization_field.key], "TEST_TEXT")

    def test_create_person_with_additional_fields(self):

        person_field = PersonField.objects.create(
            name="TEST_PERSON_FIELD",
            field_type="text",
        )

        person_field.upload()

        person_kwargs = {}
        person_kwargs['name'] = "TEST_PERSON"
        additional_fields = {}
        additional_fields[person_field.key] = "TEST_TEXT"
        person_kwargs['additional_fields'] = additional_fields

        person = Person.objects.create(**person_kwargs)

        result = person.upload()

        # The information appears locally
        self.assertTrue(result)
        self.assertIsNotNone(person.external_id)
        self.assertIsNotNone(person.name)
        self.assertIsNotNone(person.additional_fields)
        self.assertIsNotNone(person.additional_fields[person_field.key])
        self.assertEquals(person.additional_fields[person_field.key], "TEST_TEXT")

        pipedrive_api_client = Person.pipedrive_api_client

        online_person = pipedrive_api_client.get_instance(person.external_id)

        # The information appears online
        self.assertIsNotNone(online_person[u'data'])
        self.assertEquals(online_person[u'data'][u'name'], u"TEST_PERSON")
        self.assertEquals(online_person[u'data'][person_field.key], "TEST_TEXT")

    def test_create_deal_with_additional_fields(self):

        deal_field = DealField.objects.create(
            name="TEST_DEAL_FIELD",
            field_type="text",
        )

        deal_field.upload()

        deal_kwargs = {}
        deal_kwargs['title'] = "TEST_DEAL"
        deal_kwargs['pipeline_id'] = self.pipeline.external_id
        additional_fields = {}
        additional_fields[deal_field.key] = "TEST_TEXT"
        deal_kwargs['additional_fields'] = additional_fields

        deal = Deal.objects.create(**deal_kwargs)

        result = deal.upload()

        # The information appears locally
        self.assertTrue(result)
        self.assertIsNotNone(deal.external_id)
        self.assertIsNotNone(deal.title)
        self.assertIsNotNone(deal.additional_fields)
        self.assertIsNotNone(deal.additional_fields[deal_field.key])
        self.assertEquals(deal.additional_fields[deal_field.key], "TEST_TEXT")

        pipedrive_api_client = Deal.pipedrive_api_client

        online_deal = pipedrive_api_client.get_instance(deal.external_id)

        # The information appears online
        self.assertIsNotNone(online_deal[u'data'])
        self.assertEquals(online_deal[u'data'][u'title'], u"TEST_DEAL")
        self.assertEquals(online_deal[u'data'][deal_field.key], "TEST_TEXT")


class TestPipedrive(TestCase):

    def setUp(self):
        DealField.fetch_from_pipedrive()
        OrganizationField.fetch_from_pipedrive()
        PersonField.fetch_from_pipedrive()

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

    def test_datetime_from_simple_time_zero(self):

        el = {u'update_time': u'0000-00-00 00:00:00'}

        result = Organization.datetime_from_simple_time(el, u'update_time')

        self.assertIsNone(result)

    def test_datetime_from_simple_time_no_field(self):

        el = {}

        result = Organization.datetime_from_simple_time(el, u'update_time')

        self.assertIsNone(result)

    def test_datetime_from_simple_time_blank_field(self):

        el = {u'update_time': ''}

        result = Organization.datetime_from_simple_time(el, u'update_time')

        self.assertIsNone(result)

    def test_datetime_from_simple_time__field(self):

        el = {u'update_time': None}

        result = Organization.datetime_from_simple_time(el, u'update_time')

        self.assertIsNone(result)

    def test_get_value_or_none_none(self):

        el = {
            'due_time': u''
        }

        result = Activity.get_value_or_none(el, u'due_time')

        self.assertIsNone(result)

    def test_get_value_or_none_value(self):

        el = {
            'due_time': u'16:00'
        }

        result = Activity.get_value_or_none(el, u'due_time')
        expected = u'16:00'

        self.assertEquals(result, expected)

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


class TestFetchModels(TestCase):

    def test_fetch_from_pipedrive_organizations(self):

        result = Organization.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_persons(self):

        result = Person.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_deals(self):

        result = Deal.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_users(self):

        result = User.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_notes(self):

        result = Note.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_activities(self):

        result = Activity.fetch_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_from_pipedrive_pipelines(self):

        result = Pipeline.fetch_from_pipedrive()

        # TODO: wait for the API to implement properly
        self.assertTrue(result)

    def test_fetch_from_pipedrive_person_fields(self):

        result = PersonField.fetch_from_pipedrive()

        self.assertTrue(result)
        self.assertGreater(PersonField.objects.count(), 0)

    def test_fetch_from_pipedrive_organization_fields(self):

        result = OrganizationField.fetch_from_pipedrive()

        self.assertTrue(result)
        self.assertGreater(OrganizationField.objects.count(), 0)

    def test_fetch_from_pipedrive_deal_fields(self):

        result = DealField.fetch_from_pipedrive()

        self.assertTrue(result)
        self.assertGreater(DealField.objects.count(), 0)

    def test_sync_from_pipedrive(self):

        result = PipedriveModel.sync_from_pipedrive()

        self.assertTrue(result)

    def test_fetch_data_null(self):

        class fake_api():
            def get_instances(self, **kwargs):
                return {
                    "success": True,
                    "data": None,
                    "additional_data": {
                        "pagination": {
                            "start": 0,
                            "limit": 100,
                            "more_items_in_collection": False
                        }
                    }
                }

        old_api = Organization.pipedrive_api_client
        try:
            Organization.pipedrive_api_client = fake_api()
            self.assertTrue(Organization.fetch_from_pipedrive())
        finally:
            Organization.pipedrive_api_client = old_api


class TestCreateFromObject(TestCase):

    def test_activity_update_or_create_entity_from_api_post(self):

        obj = {
            u'org_name': None,
            u'deal_id': None,
            u'assigned_to_user_id': 2428657,
            u'marked_as_done_time': u'',
            u'google_calendar_id': None,
            u'done': False,
            u'duration': u'',
            u'gcal_event_id': None,
            u'subject': u'TEST_ACTIVITY',
            u'created_by_user_id': 2428657,
            u'user_id': 2428657,
            u'reference_type': u'none',
            u'company_id': 1689563,
            u'id': 2,
            u'note': u'',
            u'due_time': u'',
            u'person_id': None,
            u'type': u'call',
            u'person_dropbox_bcc': None,
            u'active_flag': True,
            u'due_date': u'2017-04-21',
            u'update_time': u'2017-04-21 12:21:10',
            u'owner_name': u'TEST_OWNER',
            u'person_name': None,
            u'deal_dropbox_bcc': None,
            u'reference_id': None,
            u'add_time': u'2017-04-21 12:21:10',
            u'google_calendar_etag': None,
            u'org_id': None,
            u'deal_title': None
        }

        result = Activity.update_or_create_entity_from_api_post(obj)

        self.assertIsNotNone(result)


class TestIntegrity(TransactionTestCase):

    def test_fetch_from_pipedrive_with_integrity_error(self):

        class fake_user_api():
            def get_instance(self, external_id):
                return {
                    "success": True,
                    "data": {
                        "id": 1629618,
                        "name": "OWNER_NAME",
                        "default_currency": "CLP",
                        "locale": "es_CL",
                        "lang": 6,
                        "email": "owner@example.com",
                        "phone": None,
                        "activated": True,
                        "last_login": "2017-04-27 10:58:25",
                        "created": "2016-08-10 00:45:36",
                        "modified": "2017-04-27 10:58:25",
                        "signup_flow_variation": None,
                        "has_created_company": True,
                        "is_admin": 1,
                        "role_id": "1",
                        "timezone_name": "America/Santiago",
                        "active_flag": True,
                        "icon_url": None,
                        "is_you": False
                    },
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

        class fake_person_api():
            def get_instance(self, external_id):
                return {
                    "success": True,
                    "data": {
                        "id": 8636,
                        "name": "PERSON",
                        'open_deals_count': 0,
                        'visible_to': 3,
                        'won_deals_count': 0,
                        'lost_deals_count': 0,
                        'closed_deals_count': 0,
                        'activities_count': 0,
                        'done_activities_count': 0,
                        'undone_activities_count': 0,
                        'email_messages_count': 0,
                    },
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

        class fake_organization_api():
            def get_instance(self, external_id):
                return {
                    "success": True,
                    "data": {
                        "id": 10105,
                        "name": "EXAMPLE ORGANIZATION",
                        'people_count': 0,
                        'open_deals_count': 0,
                        'won_deals_count': 0,
                        'lost_deals_count': 0,
                        'closed_deals_count': 0,
                        'visible_to': 3,
                        'activities_count': 0,
                        'done_activities_count': 0,
                        'undone_activities_count': 0,
                        'email_messages_count': 0,
                        'address_formatted_address': 0,
                    },
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

        class fake_stage_api():
            def get_instance(self, external_id):
                return {
                    "success": True,
                    "data": {
                        "id": 6,
                        "name": "EXAMPLE STAGE",
                        "pipeline_id": 1,
                        "order_nr": 1,
                        "active_flag": True,
                    },
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

        class fake_pipeline_api():
            def get_instance(self, external_id):
                return {
                    "success": True,
                    "data": {
                        "id": 1,
                        "name": "EXAMPLE PIPELINE",
                        "url_title": "EXAMPLE_URL_TITLE",
                        "active": True,
                    },
                    "additional_data": {
                        "company_id": 1142847
                    }
                }

        class fake_deal_api():

            deal = {
                "id": 9973,
                "creator_user_id": {
                    "id": 1629618,
                    "name": "OWNER_NAME",
                    "email": "owner@example.com",
                    "has_pic": False,
                    "pic_hash": None,
                    "active_flag": True,
                    "value": 1629618
                },
                "user_id": {
                    "id": 1629618,
                    "name": "OWNER_NAME",
                    "email": "owner@example.com",
                    "has_pic": False,
                    "pic_hash": None,
                    "active_flag": True,
                    "value": 1629618
                },
                "person_id": {
                    "name": "PERSON",
                    "email": [
                        {
                            "label": "work",
                            "value": "example@example.com",
                            "primary": True
                        }
                    ],
                    "phone": [
                        {
                            "label": "work",
                            "value": "22056282",
                            "primary": True
                        }
                    ],
                    "value": 8636
                },
                "org_id": {
                    "name": "EXAMPLE ORGANIZATION",
                    "people_count": 1,
                    "owner_id": 1629618,
                    "address": None,
                    "cc_email": "mycompany@pipedrivemail.com",
                    "value": 10105
                },
                "stage_id": 6,
                "title": "EXAMPLE DEAL",
                "value": 153.466,
                "currency": "CLP",
                "add_time": "2017-02-21 14:10:25",
                "update_time": "2017-03-02 13:39:39",
                "stage_change_time": "2017-03-02 13:39:39",
                "active": False,
                "deleted": False,
                "status": "won",
                "next_activity_date": None,
                "next_activity_time": None,
                "next_activity_id": None,
                "last_activity_id": None,
                "last_activity_date": None,
                "lost_reason": None,
                "visible_to": "1",
                "close_time": "2017-02-28 13:54:25",
                "pipeline_id": 1,
                "won_time": "2017-02-28 13:54:25",
                "first_won_time": "2017-02-28 13:54:25",
                "lost_time": None,
                "products_count": None,
                "files_count": None,
                "notes_count": 1,
                "followers_count": 1,
                "email_messages_count": None,
                "activities_count": None,
                "done_activities_count": None,
                "undone_activities_count": None,
                "reference_activities_count": None,
                "participants_count": 1,
                "expected_close_date": None,
                "last_incoming_mail_time": None,
                "last_outgoing_mail_time": None,
                "c81737a34439d1976b6b68f9f0be075c47c1b3c2": None,
                "8a766721a66bbd50506fcb65b18291b2846714b0": 1478000,
                "8a766721a66bbd50506fcb65b18291b2846714b0_currency": "CLP",
                "b7cfbad4fe7704bcdaaf7efa49cafbddfe22cac5": "https://example.com",
                "43a5a5a5febfd470155482c1a572cfe764bfe4eb": "",
                "546846b198054138ce8b5240c882517ae924ce4e": {
                    "name": "",
                    "people_count": 0,
                    "owner_id": 1629618,
                    "address": None,
                    "cc_email": "mycompany@pipedrivemail.com",
                    "value": 10110
                },
                "575333cd64992c1297dcc674cdc3191db3f1dd59": "2017-02-16",
                "cc0e1e23219765fff52a966a919351987798d6ac": None,
                "536802c95dfaa316ffea4b816438469112ca8210": None,
                "faa59be7dcd63eb42d576a19a937d37727b48524": None,
                "b8799234117d9a7233bbef58a469b759345cc87c": 122000,
                "b8799234117d9a7233bbef58a469b759345cc87c_currency": "CLP",
                "c389c981387140016623d9411fffc8feca6f8733": None,
                "c389c981387140016623d9411fffc8feca6f8733_currency": None,
                "3a2b263fe86c44c98d3abd36d56245b51b8fc51d": None,
                "4b17459584cf24172d714c6b687ada2c1ba8da88": "5",
                "3d7eb6ab9b6901d30a353d10c52362fae74ce0a3": "2017-01-25",
                "7dfd31608b5c8d4997b9434759a17b79548ebade": "rhuiza",
                "b2ea26ac273c1ed106168d9106a43ecd144aeb90": 35,
                "33b083132080c43608495304712886a40f0b9196": None,
                "stage_order_nr": 5,
                "person_name": "PERSON Del Sastre",
                "org_name": "EXAMPLE ORGANIZATION",
                "next_activity_subject": None,
                "next_activity_type": None,
                "next_activity_duration": None,
                "next_activity_note": None,
                "formatted_value": "$153",
                "rotten_time": None,
                "weighted_value": 153.466,
                "formatted_weighted_value": "$153",
                "owner_name": "OWNER_NAME",
                "cc_email": "mycompany+deal9973@pipedrivemail.com",
                "org_hidden": False,
                "person_hidden": False
            }

            def get_instances(self, **kwargs):
                return {
                    "success": True,
                    "data": [fake_deal_api.deal],
                    "additional_data": {
                        "pagination": {
                            "start": 0,
                            "limit": 100,
                            "more_items_in_collection": False,
                        }
                    },
                }

            def get_instance(self, *args, **kwargs):
                return {
                    "success": True,
                    "data": fake_deal_api.deal,
                    "additional_data": {
                        "pagination": {
                            "start": 0,
                            "limit": 100,
                            "more_items_in_collection": False,
                        }
                    },
                }

        old_deal_api = Deal.pipedrive_api_client
        old_user_api = User.pipedrive_api_client
        old_person_api = Person.pipedrive_api_client
        old_org_api = Organization.pipedrive_api_client
        old_stage_api = Stage.pipedrive_api_client
        old_pipeline_api = Pipeline.pipedrive_api_client

        try:
            Deal.pipedrive_api_client = fake_deal_api()
            User.pipedrive_api_client = fake_user_api()
            Person.pipedrive_api_client = fake_person_api()
            Organization.pipedrive_api_client = fake_organization_api()
            Stage.pipedrive_api_client = fake_stage_api()
            Pipeline.pipedrive_api_client = fake_pipeline_api()

            self.assertEquals(User.objects.count(), 0)
            self.assertEquals(Person.objects.count(), 0)
            self.assertEquals(Organization.objects.count(), 0)
            self.assertEquals(Stage.objects.count(), 0)
            self.assertEquals(Pipeline.objects.count(), 0)
            self.assertEquals(Deal.objects.count(), 0)

            Deal.sync_one(9973)

            self.assertEquals(User.objects.count(), 1)
            self.assertEquals(Person.objects.count(), 1)
            self.assertEquals(Organization.objects.count(), 1)
            self.assertEquals(Stage.objects.count(), 1)
            self.assertEquals(Pipeline.objects.count(), 1)
            self.assertEquals(Deal.objects.count(), 1)

        finally:
            Deal.pipedrive_api_client = old_deal_api
            User.pipedrive_api_client = old_user_api
            Person.pipedrive_api_client = old_person_api
            Organization.pipedrive_api_client = old_org_api
            Stage.pipedrive_api_client = old_stage_api
            Pipeline.pipedrive_api_client = old_pipeline_api


class TestUtils(TestCase):

    def test_compare_dicts(self):

        dic = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        eq = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        neq = {
            'a': 1,
            'b': 4,
            'c': 3,
        }
        sub_set = {
            'a': 1
        }
        super_set = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }

        self.assertTrue(compare_dicts(dic, eq))
        self.assertTrue(compare_dicts(eq, dic))
        self.assertFalse(compare_dicts(dic, neq))
        self.assertFalse(compare_dicts(dic, sub_set))
        self.assertFalse(compare_dicts(sub_set, dic))
        self.assertFalse(compare_dicts(dic, super_set))
        self.assertFalse(compare_dicts(super_set, dic))
        self.assertFalse(compare_dicts(None, dic))
        self.assertFalse(compare_dicts(dic, None))


class TestFields(TestCase):

    def test_truncating_char_field(self):
        person = Person.objects.create(name="a" * 1000)

        person_refresh = Person.objects.get(id=person.id)
        self.assertEquals(len(person_refresh.name), 500)


class DealTestCase(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create(name="User1", email="someemail1@mailinator.com")
        self.deal = Deal.objects.create(title="Some Deal")
        self.user_1.upload()
        self.deal.upload()
        logging.debug(self.user_1.external_id)
        logging.debug(self.deal.external_id)

    def test_change_ownership(self):

        self.deal.user_id = self.user_1.external_id
        self.deal.save()
        self.deal.upload()

        self.assertEquals(self.deal.user_id, self.user_1.external_id)
