import logging
from django.db.models.fields import CharField


class TruncatingCharField(CharField):

    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value)
        if value:
            if len(value) > self.max_length:
                logging.warning(u"Truncating to size {}: {}".format(self.max_length, value))
            return value[:self.max_length]
        return value
