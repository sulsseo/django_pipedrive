import json

from django.test import TestCase

# Create your tests here.
from pipedrive.models import Deal
from pipedrive.models import Pipeline
from test_app.models import PipedriveModelObserver


class TestPipedriveWebhooks(TestCase):

    def setUp(self):
        Deal.objects.create(
            title="TEST_DEAL",
            external_id=999,
            value=0,
        )
        Pipeline.objects.create(external_id=1)

    def test_deal_observer(self):

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
                    "user_id": 2428657,
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

        self.client.post('/pipedrive/', data=json.dumps(data), content_type="application/json")

        self.assertEquals(Deal.objects.count(), 1)

        instance = Deal.objects.get(external_id=999)

        self.assertEquals(instance.value, 1000)

        self.assertGreater(PipedriveModelObserver.count, 0)
