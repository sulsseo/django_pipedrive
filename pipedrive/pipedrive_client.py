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
        api_base_url=None,
        endpoint=None,
    ):

        self.endpoint = endpoint

        if api_base_url is None:
            api_base_url = 'https://api.pipedrive.com/v1/'
        self.api_base_url = api_base_url

        if api_key is None:
            self.api_key = settings.PIPEDRIVE_API_KEY
        else:
            self.api_key = api_key

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
    def update(self, element_id, **kwargs):
        """
        updates an element on pipedrive
        using /endpoint/:id as url
        """

        endpoint = str(self.endpoint) + '/' + str(element_id)

        restpoint = self.post_put_restify(endpoint)

        content = self.put(restpoint, kwargs)

        return content

    def get_instance(self, external_id):
        """
        Obtain the detail of an instance from the api
        """

        restpoint = self.get_restify(self.endpoint, external_id)

        content = self.get(restpoint)

        return content

    def get_instances(self, **kwargs):
        """
        Obtain a list of instances from the api
        """

        content = self.get(self.endpoint, kwargs)

        return content

    def post_instance(self, **kwargs):
        """
        Add an instance to Pipedrive
        """
        restpoint = self.post_put_restify(self.endpoint)

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
