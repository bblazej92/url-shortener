import unittest
from unittest.mock import patch

from app.main.schema import RegisterUrlSchema
from utils.exceptions import RESTValidationException


class TestRegisterUrlSchema(unittest.TestCase):

    def setUp(self):
        patch('utils.schema.base.log').start()

    def test_raises_when_original_url_missing(self):
        data = {}
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'original_url': ['Missing data for required field.'],
            }
        )

    def test_raises_when_original_url_is_too_long(self):
        data = {
            'original_url': 'http://test.pl?{}=1'.format(''.join('a' * 490))
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'original_url': ['original_url can have maximum 500 characters']
            }
        )

    def test_raises_when_slug_is_empty(self):
        data = {
            'slug': '',
            'original_url': 'http://test.pl'
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'slug': ['slug length must be between 1 and 30']
            }
        )

    def test_raises_when_slug_is_too_long(self):
        data = {
            'slug': 31 * 'a',
            'original_url': 'http://test.pl'
        }
        with self.assertRaises(RESTValidationException) as exception_cm:
            RegisterUrlSchema().load(data)

        self.assertDictEqual(
            exception_cm.exception.description,
            {
                'slug': ['slug length must be between 1 and 30']
            }
        )

    def test_raises_when_slug_contains_forbidden_special_characters(self):
        data = {
            'slug': 'te$t',
            'original_url': 'http://test.pl'
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
            'original_url': 'http://test.pl'
        }

        result = RegisterUrlSchema().load(data)

        self.assertDictEqual(result.errors, {})
        self.assertDictEqual(
            result.data,
            {
                'original_url': 'http://test.pl'
            }
        )

    def test_whole_schema_with_slug(self):
        data = {
            'slug': 'test_slug',
            'original_url': 'http://test.pl'
        }

        result = RegisterUrlSchema().load(data)

        self.assertDictEqual(result.errors, {})
        self.assertDictEqual(
            result.data,
            {
                'slug': 'test_slug',
                'original_url': 'http://test.pl'
            }
        )
