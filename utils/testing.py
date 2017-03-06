import mongoengine
import ujson as json
import unittest

from flask.testing import FlaskClient
from pip.utils import cached_property
from werkzeug.wrappers import BaseResponse

from app import create_app


def login_user(client, user):
    with client.session_transaction() as session:
        session['user_id'] = str(user.id)


class JsonResponse(BaseResponse):

    @cached_property
    def json(self):
        return json.loads(self.data)


class JsonTestClient(FlaskClient):

    def post(self, *args, **kwargs):
        kwargs['data'] = json.dumps(kwargs['data'])
        kwargs['content_type'] = 'application/json'
        return super(JsonTestClient, self).post(*args, **kwargs)


class ViewFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.test_client_class = JsonTestClient
        self.app.response_class = JsonResponse
        self.client = self.app.test_client()
        self.db = mongoengine.connection.get_db()

    def tearDown(self):
        for collection in self.db.collection_names():
            self.db.drop_collection(collection)
        self.app_context.pop()
