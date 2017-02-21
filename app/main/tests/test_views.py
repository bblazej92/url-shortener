import datetime
from unittest.mock import patch

import freezegun
from app.models import ShortLink, User
from dateutil import parser
from dateutil.tz import tzutc
from utils.testing import ViewFunctionalTest


# TODO: test that schema is called

class TestRegisterUrlFunctional(ViewFunctionalTest):

    def setUp(self):
        super(TestRegisterUrlFunctional, self).setUp()
        patch('app.main.views.log').start()
        self.user = User()
        self.user.save()
        with self.client.session_transaction() as session:
            session['user_id'] = str(self.user.id)

    @freezegun.freeze_time('2017-02-01T12:00:00')
    @patch('app.main.views.hex_to_base64')
    def test_if_only_original_url_specified(self, hex_to_base64_mock,):
        hex_to_base64_mock.return_value = 'mock_slug'

        url_data = dict(original_url='http://destination.pl')

        response = self.client.post('/register_url', data=url_data)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, dict(short_url='http://test.pl/mock_slug'))

        short_links = ShortLink.objects()
        self.assertEqual(len(short_links), 1)

        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://destination.pl')
        self.assertEqual(short_link.slug, 'mock_slug')
        self.assertEqual(short_link.user_id, str(self.user.id))
        self.assertEqual(short_link.id.generation_time, datetime.datetime(2017, 2, 1, 12, 0, tzinfo=tzutc()))

    @freezegun.freeze_time('2017-02-01T12:00:00')
    def test_if_unique_slug_specified(self):
        url_data = dict(original_url='http://destination.pl', slug='test_slug')

        response = self.client.post('/register_url', data=url_data)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, dict(short_url='http://test.pl/test_slug'))

        short_links = ShortLink.objects()
        self.assertEqual(len(short_links), 1)

        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://destination.pl')
        self.assertEqual(short_link.slug, 'test_slug')
        self.assertEqual(short_link.user_id, str(self.user.id))
        self.assertEqual(short_link.id.generation_time, datetime.datetime(2017, 2, 1, 12, 0, tzinfo=tzutc()))

    def test_if_non_unique_slug_specified(self):
        new_user = User()
        new_user.save()
        ShortLink(original_url='http://test.pl', slug='test_slug', user_id=str(new_user.id)).save()
        url_data = dict(original_url='http://destination.pl', slug='test_slug')

        response = self.client.post('/register_url', data=url_data)

        self.assertEqual(response.status_code, 500)
        short_links = ShortLink.objects()
        self.assertEqual(len(short_links), 1)
        short_link = short_links[0]
        self.assertEqual(short_link.original_url, 'http://test.pl')
        self.assertEqual(short_link.user_id, str(new_user.id))
        self.assertEqual(short_link.slug, 'test_slug')

    def test_if_slug_generated_from_object_id_was_added_as_custom_slug_earlier(self):
        # TODO
        pass


class TestGetUrlFunctional(ViewFunctionalTest):

    def setUp(self):
        super(TestGetUrlFunctional, self).setUp()
        patch('app.main.views.log').start()

    def test_if_slug_not_in_db(self):
        slug = 'test'

        response = self.client.get('/{}'.format(slug))

        self.assertEqual(response.status_code, 404)

    def test_if_slug_in_db(self):
        slug = 'test'
        ShortLink(original_url='http://test.pl', slug=slug).save()

        response = self.client.get('/{}'.format(slug))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, dict(original_url='http://test.pl'))

    def test_if_duplicated_slug_in_db(self):
        slug = 'test'
        ShortLink(original_url='http://test.pl', slug=slug).save()
        ShortLink(original_url='http://test2.pl', slug=slug).save()

        response = self.client.get('/{}'.format(slug))

        self.assertEqual(response.status_code, 500)


class TestGetUrlInfoFunctional(ViewFunctionalTest):

    def setUp(self):
        super(TestGetUrlInfoFunctional, self).setUp()
        patch('app.main.views.log').start()
        self.user = User()
        self.user.save()
        with self.client.session_transaction() as session:
            session['user_id'] = str(self.user.id)

    def test_if_slug_not_in_db(self):
        slug = 'test'

        response = self.client.get('/url_info/{}'.format(slug))

        self.assertEqual(response.status_code, 404)

    def test_if_duplicated_slug_in_db(self):
        slug = 'test'
        ShortLink(original_url='http://test.pl', slug=slug, user_id=str(self.user.id)).save()
        ShortLink(original_url='http://test2.pl', slug=slug, user_id=str(self.user.id)).save()

        response = self.client.get('/url_info/{}'.format(slug))

        self.assertEqual(response.status_code, 500)

    def test_if_slug_in_db_but_other_user_is_slug_owner(self):
        other_user = User()
        other_user.save()
        slug = 'test'
        ShortLink(original_url='http://test.pl', slug=slug, user_id=str(other_user.id)).save()

        response = self.client.get('/url_info/{}'.format(slug))

        self.assertEqual(response.status_code, 401)

    @freezegun.freeze_time('2017-02-01T12:00:00')
    def test_if_slug_in_db_and_user_is_its_owner(self):
        slug = 'test'
        ShortLink(
            original_url='http://test.pl',
            slug=slug,
            user_id=str(self.user.id),
        ).save()

        response = self.client.get('/url_info/{}'.format(slug))
        response.json['created'] = parser.parse(response.json['created'])

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json,
            dict(
                original_url='http://test.pl',
                created=datetime.datetime(2017, 2, 1, 12, 0, 0, tzinfo=tzutc())
            )
        )
