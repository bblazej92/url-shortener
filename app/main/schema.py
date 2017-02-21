from marshmallow import fields
from marshmallow import validate
from marshmallow.validate import Length

from utils.schema.base import ViewBaseSchema


class RegisterUrlSchema(ViewBaseSchema):

    ALLOWED_SPECIAL_CHARACTERS = ['_', '\-']

    original_url = fields.Url(
        required=True,
        validate=Length(max=500, error='original_url can have maximum 500 characters')
    )
    slug = fields.String(
        validate=[
            validate.Length(min=1, max=30, error='slug length must be between 1 and 30'),
            validate.Regexp(
                r'[a-zA-Z0-9{}]*$'.format(''.join(ALLOWED_SPECIAL_CHARACTERS)),
                error='slug contains special characters different than _ and -'
            )
        ]
    )
