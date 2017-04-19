# Create your tests here.

import pytz
import datetime

from django.test import TestCase

from pipedrive.models import Deal
from pipedrive.models import Person
from pipedrive.models import Organization
from pipedrive.models import PersonField
from pipedrive.models import DealField
from pipedrive.models import OrganizationField
from pipedrive.models import Pipeline
from pipedrive.models import Stage


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