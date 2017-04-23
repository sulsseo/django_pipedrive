import json
import logging

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from django.http import HttpResponse
from django.http import HttpResponseServerError


from pipedrive.models import Deal
from pipedrive.models import Person
from pipedrive.models import Organization
from pipedrive.models import Note
from pipedrive.models import Activity
from pipedrive.models import Pipeline
from pipedrive.models import Stage
from pipedrive.models import PipedriveModel


class NonImplementedVersionException(Exception):
    pass


# Create your views here.
@csrf_exempt
def index(request):

    try:
        if request.method == 'POST':

            json_data = json.loads(request.body)
            meta = json_data[u'meta']

            # API v1
            if meta[u'v'] == 1:
                return handle_v1(json_data)
            else:
                raise NonImplementedVersionException()

    except IntegrityError as e:
        logging.error(e.message)
        logging.error("Forcing full sync from pipedrive")
        PipedriveModel.sync_from_pipedrive()

    return HttpResponse("Hello, world!")


def handle_v1(json_data):

    meta = json_data[u'meta']

    object_type = meta[u'object']
    action = meta[u'action']
    external_id = meta[u'id']

    model = map_models(object_type)

    previous = json_data[u'previous']
    current = json_data[u'current']

    try:

        if action == 'updated':

            # The corresponding instance is found for update
            instance = model.objects.get(external_id=external_id)

            # Compute difference between previous and current
            diffkeys = [k for k in previous if previous[k] != current[k]]

            for key in diffkeys:
                value = current[key]
                setattr(instance, key, value)

            instance.save()

        if action == 'added':

            # Object's key name is changed
            current['external_id'] = current.pop('id')

            # Fields from the API that are not localy recognized
            # by the model are filtered
            current = filter_fields(current, model)
            current = fix_fields(current)

            model.objects.create(**current)

        if action == 'deleted':

            # The corresponding instance is found for delete
            instance = model.objects.get(external_id=external_id)

            # The instance is not actually deleted, but marked as deleted
            instance.deleted = True
            instance.save()

        if action == 'merged':

            # The corresponding instance is found for update
            instance = model.objects.get(external_id=external_id)

    except Activity.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)
    except Deal.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)
    except Person.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)
    except Organization.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)
    except Note.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)
    except Pipeline.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)
    except Stage.DoesNotExist as e:
        handle_does_not_exist(e, external_id, json_data)


    return HttpResponse("OK!")

def handle_does_not_exist(e, external_id, json_data):
    logging.error(e.message)
    logging.error("Forcing single sync from pipedrive")
    model.sync_one(external_id)
    handle_v1(json_data)


def map_models(object_type):
    return {
        'deal': Deal,
        'person': Person,
        'organization': Organization,
        'note': Note,
        'activity': Activity,
        'pipeline': Pipeline,
        'stage': Stage
    }[object_type]


def filter_fields(data, model):

    keylist = [k.attname for k in model._meta.concrete_fields]

    for k in data.keys():
        if k not in keylist:
            data.pop(k)

    return data


def fix_fields(data):
    """
    fix_fields fixes type issues with some fields
    for example marked_as_done_time datetime field appears
    as '' instead of None
    """
    for k in data.keys():
        if k == u'marked_as_done_time' and data[k] == u'':
            data[k] = None

    return data
