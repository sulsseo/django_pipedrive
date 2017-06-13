import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from django.http import HttpResponse

from pipedrive.models import Deal
from pipedrive.models import Person
from pipedrive.models import Organization
from pipedrive.models import Note
from pipedrive.models import Activity
from pipedrive.models import Pipeline
from pipedrive.models import Stage
from pipedrive.models import PipedriveModel
from pipedrive.models import FieldModification


class NonImplementedVersionException(Exception):
    pass


# Create your views here.
@csrf_exempt
def index(request):

    enable_hstore()

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
        logging.warning(e.message)
        logging.warning("Forcing full sync from pipedrive")
        PipedriveModel.sync_from_pipedrive()

    return HttpResponse("Hello, world!")


def enable_hstore():

    # HACK to use hstore in commands
    # source: https://github.com/djangonauts/django-hstore/issues/141

    from django.db import connection
    from psycopg2.extras import register_hstore
    # And then in `def handle`
    register_hstore(connection.cursor(), globally=True, unicode=True)


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

            instance = model.objects.get(external_id=external_id)

            FieldModification.create_modifications(instance, previous, current)

            model.update_or_create_entity_from_api_post(current)

        if action == 'added':

            model.update_or_create_entity_from_api_post(current)

        if action == 'deleted':

            # The corresponding instance is found for delete
            instance = model.objects.get(external_id=external_id)

            FieldModification.create_modifications(
                instance,
                {'deleted': instance.deleted},
                {'deleted': True}
            )

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
    logging.warning(e.message)
    logging.warning("Forcing full sync from pipedrive")
    PipedriveModel.sync_from_pipedrive()
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
