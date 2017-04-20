import json

from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseServerError

from pipedrive.models import Deal
from pipedrive.models import Person
from pipedrive.models import Organization

class NonImplementedVersionException(Exception):
    pass

# Create your views here.
def index(request):

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            meta = json_data[u'meta']

            # API v1
            if meta[u'v'] == 1:
                return handle_v1(json_data)
            else:
                raise NonImplementedVersionException


        except KeyError:
            HttpResponseServerError("Malformed data!")

    return HttpResponse("Hello, world!")

def handle_v1(json_data):

    meta = json_data[u'meta']

    object_type = meta[u'object']
    action = meta[u'action']
    external_id = meta[u'id']

    model = map_models(object_type)
    

    previous = json_data[u'previous']
    current = json_data[u'current']

    if action == 'updated':

        instance = model.objects.get(external_id=external_id)

        diffkeys = [k for k in previous if previous[k] != current[k]]

        for key in diffkeys:
            value = current[key]
            setattr(instance, key, value)

        instance.save()

    if action == 'added':
        current['external_id'] = current.pop('id')

        current = filter_fields(current, model)

        model.objects.create(**current)

    return HttpResponse("OK!")

def map_models(object_type):
    return {
        'deal': Deal,
        'person': Person,
        'organization': Organization,
    }[object_type]

def filter_fields(data, model):

    keylist = [k.attname for k in model._meta.concrete_fields]
    
    for k in data.keys():
        if k not in keylist:
            data.pop(k)

    return data