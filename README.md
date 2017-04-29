# django_pipedrive

[![CircleCI](https://circleci.com/gh/MasAval/django_pipedrive.svg?style=svg)](https://circleci.com/gh/MasAval/django_pipedrive)
[![codecov](https://codecov.io/gh/MasAval/django_pipedrive/branch/master/graph/badge.svg)](https://codecov.io/gh/MasAval/django_pipedrive)

django_pipedrive is a simple Django app to post data to the Pipedrive service and keep track of its online data. 
The app listens for the Pipedrive webhooks for every event as for version 1 of the API.

Quick start
-----------

1. Add "django_pipedrive" to your INSTALLED_APPS setting like this::

```python
    INSTALLED_APPS = (
        ...
        'django_pipedrive',
    )
```

2. Configure the variable "PIPEDRIVE_API_KEY" in settings like this::

```python

    PIPEDRIVE_API_KEY="your_actual_pipedrive_api_key"
```

3. Include the django_pipedrive URLconf in your project urls.py like this::
```python
    url(r'^django_pipedrive/', include('django_pipedrive.urls')),
```
4. Run `python manage.py migrate` to create the django_pipedrive models.

5. Start the development server and visit http://127.0.0.1:8000/django_pipedrive/
   to verify that the server is listening for webhooks (you'll just read a Hello World, but that is enough to check that the server is working).

6. Register the url as a webhook at https://yourdomain.pipedrive.com/webhooks
 
## Available Models

- pipedrive.User
- pipedrive.Pipeline
- pipedrive.Stage
- pipedrive.Person
- pipedrive.Organization
- pipedrive.Deal
- pipedrive.Activity
- pipedrive.Note

### Model conventions

All models have field called 'external_id' which is the corresponding 'id' at Pipedrive.

## Compatibility

The app has been tested with Django1.8 and Postgres 9.5.6

## Caveats

As for the first version of the app, it requires the extension HStore of postgres to deal with Pipedrive's custom fields