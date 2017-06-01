import logging

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from pipedrive.models import Deal


class PipedriveModelObserver(models.Model):

    count = 0

    @receiver(post_save, sender=Deal)
    def my_callback(sender, **kwargs):

        PipedriveModelObserver.count = PipedriveModelObserver.count + 1

        logging.debug(u"PipedriveModelObserver.count: {}".format(PipedriveModelObserver.count))
