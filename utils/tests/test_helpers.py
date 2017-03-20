import unittest
from unittest.mock import patch

from utils.helpers import generate_random_slug, SLUG_ALLOWED_CHARACTERS


class TestGenerateRandomSlug(unittest.TestCase):

    def test_length_equal_to_specified(self):
        slug = generate_random_slug(length=10)

        self.assertEqual(len(slug), 10)

    @patch('utils.helpers.choice')
    def test_choose_characters_from_allowed_characters_list(self, random_choice_mock):
        random_choice_mock.side_effect = 'A' * 5

        slug = generate_random_slug(length=5)

        self.assertEqual(slug, 'AAAAA')
        random_choice_mock.asssert_called_with(SLUG_ALLOWED_CHARACTERS)
