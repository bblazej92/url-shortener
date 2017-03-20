import datetime
from unittest.mock import patch

import freezegun
from app.models import ShortUrl, User
from dateutil import parser
from dateutil.tz import tzutc
from flask import url_for
from utils.testing import ViewFunctionalTest, login_user


class TestRegisterUrlFunctional(ViewFunctionalTest):
    ENDPOINT = '/v1/generate_short_url'

    def setUp(self):
        super(TestRegisterUrlFunctional, self).setUp()
        patch('app.main.views.log').start()
        patch('utils.schema.base.log').start()
        self.user = User()
        self.user.save()

    def test_login_required(self):
        url_data = dict(original_url='http://destination.pl')

        response = self.client.post(self.ENDPOINT, data=url_data)

        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('auth.oauth_authorize'), response.headers['Location'])

    def test_schema_validation_applied(self):
        login_user(self.client, self.user)
        url_data = dict(original_url='incorrect_url.pl')

        response = self.client.post(self.ENDPOINT, data=url_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'SchemaValidationErrors', response.data)

    @freezegun.freeze_time('2017-02-01T12:00:00')
    @patch('app.main.views.generate_random_slug')
    def test_when_only_original_url_specified_and_generated_slug_is_unique(self, generate_random_slug_mock):
        login_user(self.client, self.user)
        generate_random_slug_mock.return_value = 'test_slug'
        url_data = dict(original_url='http://destination.pl')

        response = self.client.post(self.ENDPOINT, data=url_data)

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json, dict(short_url='http://localhost:5001/test_slug'))
        short_links = ShortUrl.objects()
        self.assertEqual(len(short_links), 1)
        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://destination.pl')
        self.assertEqual(short_link.slug, 'test_slug')
        self.assertEqual(short_link.user_id, str(self.user.id))
        self.assertEqual(short_link.access_counter, 0)
        self.assertEqual(short_link.created, datetime.datetime(2017, 2, 1, 12, 0, tzinfo=tzutc()))

    @freezegun.freeze_time('2017-02-01T12:00:00')
    @patch('app.main.views.generate_random_slug')
    def test_when_only_original_url_specified_and_generated_slug_already_exist(self, generate_random_slug_mock):
        login_user(self.client, self.user)
        generate_random_slug_mock.side_effect = ['test_slug', 'new_slug']
        ShortUrl(original_url='http://test.pl', slug='test_slug').save()
        url_data = dict(original_url='http://destination.pl')

        short_links = ShortUrl.objects()
        self.assertEqual(len(short_links), 1)

        response = self.client.post(self.ENDPOINT, data=url_data)

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json, dict(short_url='http://localhost:5001/new_slug'))
        short_links = ShortUrl.objects(slug__ne='test_slug')
        self.assertEqual(len(short_links), 1)
        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://destination.pl')
        self.assertEqual(short_link.slug, 'new_slug')
        self.assertEqual(short_link.user_id, str(self.user.id))
        self.assertEqual(short_link.access_counter, 0)
        self.assertEqual(short_link.created, datetime.datetime(2017, 2, 1, 12, 0, tzinfo=tzutc()))

    @freezegun.freeze_time('2017-02-01T12:00:00')
    def test_when_unique_slug_specified(self):
        login_user(self.client, self.user)
        url_data = dict(original_url='http://destination.pl', slug='test_slug')

        response = self.client.post(self.ENDPOINT, data=url_data)

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json, dict(short_url='http://localhost:5001/test_slug'))
        short_links = ShortUrl.objects()
        self.assertEqual(len(short_links), 1)
        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://destination.pl')
        self.assertEqual(short_link.slug, 'test_slug')
        self.assertEqual(short_link.user_id, str(self.user.id))
        self.assertEqual(short_link.access_counter, 0)
        self.assertEqual(short_link.created, datetime.datetime(2017, 2, 1, 12, 0, tzinfo=tzutc()))

    def test_when_non_unique_slug_specified(self):
        login_user(self.client, self.user)
        new_user = User()
        new_user.save()
        ShortUrl(original_url='http://test.pl', slug='test_slug', user_id=str(new_user.id)).save()
        url_data = dict(original_url='http://destination.pl', slug='test_slug')

        response = self.client.post(self.ENDPOINT, data=url_data)

        self.assertEqual(response.status_code, 500)
        short_links = ShortUrl.objects()
        self.assertEqual(len(short_links), 1)
        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://test.pl')
        self.assertEqual(short_link.user_id, str(new_user.id))
        self.assertEqual(short_link.slug, 'test_slug')


class TestGetUrlFunctional(ViewFunctionalTest):
    ENDPOINT_TEMPLATE = '/{}'

    def setUp(self):
        super(TestGetUrlFunctional, self).setUp()
        patch('app.main.views.log').start()

    def test_when_slug_not_in_db(self):
        slug = 'test'

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 404)

    def test_when_slug_in_db(self):
        slug = 'test'
        ShortUrl(original_url='http://test.pl', slug=slug).save()

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, dict(original_url='http://test.pl'))

    def test_when_duplicated_slug_in_db(self):
        slug = 'test'
        ShortUrl(original_url='http://test.pl', slug=slug).save()
        ShortUrl(original_url='http://test2.pl', slug=slug).save()

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 500)


class TestGetUrlInfoFunctional(ViewFunctionalTest):
    ENDPOINT_TEMPLATE = '/v1/url_info/{}'

    def setUp(self):
        super(TestGetUrlInfoFunctional, self).setUp()
        patch('app.main.views.log').start()
        self.user = User()
        self.user.save()

    def test_login_required(self):
        slug = 'test'

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('auth.oauth_authorize'), response.headers['Location'])

    def test_when_slug_not_in_db(self):
        login_user(self.client, self.user)
        slug = 'test'

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 404)

    def test_when_duplicated_slug_in_db(self):
        login_user(self.client, self.user)
        slug = 'test'
        ShortUrl(original_url='http://test.pl', slug=slug, user_id=str(self.user.id)).save()
        ShortUrl(original_url='http://test2.pl', slug=slug, user_id=str(self.user.id)).save()

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 500)

    def test_when_slug_in_db_but_other_user_is_slug_owner(self):
        login_user(self.client, self.user)
        other_user = User()
        other_user.save()
        slug = 'test'
        ShortUrl(original_url='http://test.pl', slug=slug, user_id=str(other_user.id)).save()

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))

        self.assertEqual(response.status_code, 401)

    @freezegun.freeze_time('2017-02-01T12:00:00')
    def test_when_slug_in_db_and_user_is_its_owner(self):
        login_user(self.client, self.user)
        slug = 'test'
        ShortUrl(
            original_url='http://test.pl',
            slug=slug,
            user_id=str(self.user.id),
        ).save()

        response = self.client.get(self.ENDPOINT_TEMPLATE.format(slug))
        response.json['created'] = parser.parse(response.json['created'])

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json,
            dict(
                original_url='http://test.pl',
                created=datetime.datetime(2017, 2, 1, 12, 0, 0, tzinfo=tzutc()),
                access_counter=0
            )
        )

    def test_access_counter_increases(self):
        login_user(self.client, self.user)
        slug = 'test'
        url_data = dict(original_url='http://destination.pl', slug=slug)

        self.client.post('/v1/generate_short_url', data=url_data)
        self.client.get('/{}'.format(slug))
        self.client.get('/{}'.format(slug))

        short_link = ShortUrl.objects.get(slug=slug)
        self.assertEqual(short_link.access_counter, 2)


class TestGetListOfUserUrlsFunctional(ViewFunctionalTest):
    ENDPOINT = '/v1/list_urls'

    def setUp(self):
        super(TestGetListOfUserUrlsFunctional, self).setUp()
        patch('app.main.views.log').start()
        self.user = User()
        self.user.save()

    def test_login_required(self):
        response = self.client.get(self.ENDPOINT)

        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('auth.oauth_authorize'), response.headers['Location'])

    def test_when_user_has_no_url_created(self):
        login_user(self.client, self.user)
        response = self.client.get(self.ENDPOINT)

        self.assertEqual(response.json, {'URLs': []})

    @freezegun.freeze_time('2017-02-01T12:00:00')
    def test_when_user_has_one_url_created(self):
        login_user(self.client, self.user)
        ShortUrl(original_url='http://test.pl', slug='test', user_id=str(self.user.id)).save()

        response = self.client.get(self.ENDPOINT)

        self.assertEqual(
            response.json,
            {
                'URLs': [{
                    'slug': 'test',
                    'original_url': 'http://test.pl',
                    'created': '2017-02-01T12:00:00+00:00',
                    'access_counter': 0
                }]
            }
        )

    @freezegun.freeze_time('2017-02-01T12:00:00')
    def test_when_user_has_many_urls_created(self):
        login_user(self.client, self.user)
        ShortUrl(original_url='http://test.pl', slug='test', user_id=str(self.user.id)).save()
        ShortUrl(original_url='http://test2.pl', slug='test2', user_id=str(self.user.id)).save()

        response = self.client.get(self.ENDPOINT)

        self.assertEqual(
            response.json,
            {
                'URLs': [
                    {
                        'slug': 'test',
                        'original_url': 'http://test.pl',
                        'created': '2017-02-01T12:00:00+00:00',
                        'access_counter': 0
                    },
                    {
                        'slug': 'test2',
                        'original_url': 'http://test2.pl',
                        'created': '2017-02-01T12:00:00+00:00',
                        'access_counter': 0
                    }
                ]
            }
        )
