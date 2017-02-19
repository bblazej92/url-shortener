from flask import logging
from marshmallow import Schema

from utils.exceptions import RESTValidationException

log = logging.getLogger(__name__)


def handle_view_errors(schema, errors, obj):
    if errors:
        log.error(errors)
        raise RESTValidationException(errors)


class ViewBaseSchema(Schema):
    __error_handler__ = handle_view_errors
