from unittest.mock import patch

from utils.testing import ViewFunctionalTest

# TODO: test that schema is called


class TestRegisterUrl(ViewFunctionalTest):

    @patch('app.main.views.hex_to_base64')
    def test_registers_url_if_only_destination_url_specified(self, hex_to_base64_mock):
        hex_to_base64_mock.return_value = 'mock_slug'
        url_data = dict(destination_url='http://destination.pl')

        response = self.client.post('/register_url', data=url_data)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, dict(short_url='http://test.pl/mock_slug'))
