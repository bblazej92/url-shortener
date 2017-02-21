import unittest
from unittest.mock import patch

from app.main.schema import RegisterUrlSchema
from utils.exceptions import RESTValidationException


class TestRegisterUrlSchema(unittest.TestCase):

    def setUp(self):
        patch('utils.schema.base.log').start()

    def test_raises_if_destination_url_missing(self):
        data = {}
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'destination_url': ['Missing data for required field.'],
            }
        )

    def test_raises_if_destination_url_is_too_long(self):
        data = {
            'destination_url': 'http://test.pl?{}=1'.format(''.join('a' * 490))
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'destination_url': ['destination_url can have maximum 500 characters']
            }
        )

    def test_raises_if_slug_is_empty(self):
        data = {
            'slug': '',
            'destination_url': 'http://test.pl'
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'slug': ['slug length must be between 1 and 30']
            }
        )

    def test_raises_if_slug_is_too_long(self):
        data = {
            'slug': 31 * 'a',
            'destination_url': 'http://test.pl'
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'slug': ['slug length must be between 1 and 30']
            }
        )

    def test_raises_if_slug_contains_forbidden_special_characters(self):
        data = {
            'slug': 'te$t',
            'destination_url': 'http://test.pl'
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'slug': ['slug contains special characters different than _ and -']
            }
        )

    def test_whole_schema_without_slug(self):
        data = {
            'destination_url': 'http://test.pl'
        }

        result = RegisterUrlSchema().load(data)

        self.assertDictEqual(result.errors, {})
        self.assertDictEqual(
            result.data,
            {
                'destination_url': 'http://test.pl'
            }
        )

    def test_whole_schema_with_slug(self):
        data = {
            'slug': 'test_slug',
            'destination_url': 'http://test.pl'
        }

        result = RegisterUrlSchema().load(data)

        self.assertDictEqual(result.errors, {})
        self.assertDictEqual(
            result.data,
            {
                'slug': 'test_slug',
                'destination_url': 'http://test.pl'
            }
        )
