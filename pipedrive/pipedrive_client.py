# -*- encoding: utf-8 -*-

# standard library
import json
import urlparse
import time

# requests
import requests
from django.conf import settings


class PipedriveAPIClient(object):

    def __init__(
        self,
        api_key=None,
        email=None,
        password=None,
        api_base_url=None
    ):

        if api_base_url is None:
            api_base_url = 'https://api.pipedrive.com/v1/'
        self.api_base_url = api_base_url

        if api_key is None:
            self.api_key = settings.PIPEDRIVE_API_KEY
        else:
            self.api_key = PIPEDRIVE_API_KEY

        super(PipedriveAPIClient, self).__init__()

    def call_api(self, method, endpoint, payload):
        url = urlparse.urljoin(self.api_base_url, endpoint)

        if method == 'POST':
            response = requests.post(url, data=payload)
            # response = requests.post(url, data=json.dumps(payload))
        elif method == 'delete':
            response = requests.delete(url)
        elif method == 'put':
            response = requests.put(url, data=payload)
        else:
            if self.api_key:
                payload.update({'api_token': self.api_key})
            response = requests.get(url, params=payload)

        content = json.loads(response.content)

        # self.request_limit(response)

        return content

    def get(self, endpoint, payload=None):
        if payload is None:
            payload = {}

        return self.call_api('get', endpoint, payload)

    def post(self, endpoint, payload):
        return self.call_api('POST', endpoint, payload)

    def put(self, endpoint, payload):
        return self.call_api('put', endpoint, payload)

    def delete(self, endpoint):
        return self.call_api('delete', endpoint, payload=None)

    # put methods
    def update(self, endpoint, element_id, payload):
        """
        updates an element on pipedrive
        using /endpoint/:id as url
        """

        endpoint = str(endpoint) + '/:' + str(element_id)

        restpoint = self.post_put_restify(endpoint)

        content = self.put(restpoint, payload)

        return content

    def update_deal(self, deal, **kwargs):
        """
        updates a deal on pipedrive
        """
        updatepoint = 'deals'

        endpoint = str(updatepoint) + '/:' + str(deal.id)

        restpoint = self.post_put_restify(endpoint)

        content = self.put(restpoint, kwargs)

        return content

    # get methods
    def get_pipeline_stages(self):
        """
        get all pipelines from pipedrive
        """
        endpoint = 'pipelines'

        content = self.get(endpoint)

        return content

    def get_stages(self):
        """
        get all stages from pipedrive
        """
        endpoint = 'stages'

        content = self.get(endpoint)

        return content

    def get_deal(self, deal):
        """
        Obtain the detail of a deal from the api
        """
        deal_id = deal.external_id

        endpoint = 'deals'

        restpoint = self.get_restify(endpoint, deal_id)

        content = self.get(restpoint)

        return content

    def get_deals(self, **kwargs):
        """
        Obtain a list of deals from the api
        """
        endpoint = 'deals'

        content = self.get(endpoint, kwargs)

        return content

    def get_deal_fields(self, **kwargs):
        """
        Obtain a list of deals from the api
        """
        endpoint = 'dealFields'

        content = self.get(endpoint, kwargs)

        return content

    def get_person(self, person):
        """
        Obtain details of a single person
        """
        person_id = person.external_id

        endpoint = 'persons'

        restpoint = self.get_restify(endpoint, person_id)

        content = self.get(restpoint)

        return content

    def get_persons(self, **kwargs):
        """
        Obtain a list of persons from the api
        """
        endpoint = 'persons'

        content = self.get(endpoint, kwargs)

        return content

    def get_person_fields(self, **kwargs):
        """
        Get persons base and custom fields
        """
        endpoint = 'personFields'

        content = self.get(endpoint, kwargs)

        return content

    def get_organization(self, organization):
        """
        Obtain details of a single person
        """
        organization_id = organization.external_id

        endpoint = 'organizations'

        restpoint = self.get_restify(endpoint, organization_id)

        content = self.get(restpoint)

        return content

    def get_organizations(self, **kwargs):
        """
        Obtain a list of organization from the api
        """
        endpoint = 'organizations'

        content = self.get(endpoint, kwargs)

        return content

    def get_users(self, **kwargs):
        """
        Obtain a list of users from the api
        """
        endpoint = 'users'

        content = self.get(endpoint, kwargs)

        return content

    def get_notes(self, **kwargs):
        """
        Obtain a list of notes from the api
        """
        endpoint = 'notes'

        content = self.get(endpoint, kwargs)

        return content

    def get_organization_fields(self, **kwargs):
        """
        Get organization fields & custom fields
        """
        endpoint = 'organizationFields'

        content = self.get(endpoint, kwargs)

        return content

    # post methods
    def post_deal(self, **kwargs):
        """
        Add a deal to Pipedrive
        'title' is required
        """
        endpoint = 'deals'

        restpoint = self.post_put_restify(endpoint)

        content = self.post(restpoint, kwargs)

        return content

    def post_person(self, **kwargs):
        """
        Add a person to Pipedrive and saves
        the person's external id to model.Person
        'name' is required
        """
        endpoint = 'persons'

        restpoint = self.post_put_restify(endpoint)

        content = self.post(restpoint, kwargs)

        return content

    def post_organization(self, **kwargs):
        """
        Add a organization to Pipedrive
        'name' is required
        """
        endpoint = 'organizations'

        restpoint = self.post_put_restify(endpoint)

        content = self.post(restpoint, kwargs)

        return content

    def get_restify(self, endpoint, pk):
        """
        Creates and returns a valid Pipedrive url for
        get method on single items
        """

        restful = (
            str(endpoint) +
            '/' +
            str(pk)
        )

        return restful

    def post_put_restify(self, endpoint):
        """
        Creates and retuns a valid Pipedrive url for
        post method
        """

        restful = (
            str(endpoint) +
            '?api_token=' +
            str(self.api_key)
        )

        return restful

    def authenticate(self, email=None, password=None):
        """
        Fetches an api token from Pipedrive.
        If no params are given this method will
        first try to use self's email and pass, if
        those values are None then it will use the
        values from the settings file.
        """
        if email and password:
            endpoint = 'authorizations'
            payload = {
                'email': email,
                'password': password,
            }

            content = self.post(endpoint, payload)

            for dict_list in content['data']:
                if dict_list['api_token']:
                    self.api_key = dict_list['api_token']

        else:
            try:
                self.authenticate(self.email, self.password)
            except:
                email = settings.PIPEDRIVE_ADMIN_EMAIL
                password = settings.PIPEDRIVE_ADMIN_PASS

                self.email = email
                self.password = password
                self.authenticate(email, password)

    def get_keys_list(self, fields_data):

        keys_list = []
        for dict_key in fields_data['data']:
            if dict_key['key']:
                keys_list.append(dict_key['key'])

        return keys_list

    def get_data_list(self, data):
        """
        Simple shortcut that returns a list of
        all dictionaries inside the 'data' list
        of pipedrive response
        """
        try:
            if data['data']:
                data_list = data['data']
        except:
            data_list = []

        return data_list

    def request_limit(self, response):
        if response.headers['x-ratelimit-remaining'] < 2:
            time.sleep(9)