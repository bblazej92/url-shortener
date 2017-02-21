from werkzeug.exceptions import BadRequest, InternalServerError


class RESTValidationException(BadRequest):

    def __init__(self, errors, *args, **kwargs):
        super(RESTValidationException, self).__init__(*args, **kwargs)
        self.description = errors


class SlugAlreadyExistsException(InternalServerError):
    pass
