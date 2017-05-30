# -*- encoding: utf-8 -*-

# standard library
import json
import urlparse

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
        elif method == 'delete':
            response = requests.delete(url)
        elif method == 'put':
            response = requests.put(url, data=payload)
        else:
            if self.api_key:
                payload.update({'api_token': self.api_key})
            response = requests.get(url, params=payload)

        content = json.loads(response.content)

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

        restpoint = self.restify(endpoint)

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
        restpoint = self.restify(self.endpoint)

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

    def restify(self, endpoint):
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

    def delete_instance(self, element_id):

        endpoint = str(self.endpoint) + '/' + str(element_id)

        restpoint = self.restify(endpoint)

        content = self.delete(restpoint)

        return content
