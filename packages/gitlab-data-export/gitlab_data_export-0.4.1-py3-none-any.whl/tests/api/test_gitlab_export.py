
import unittest
import os

import gitlab_data_export.api.gitlab_export as gitlab_api


class TestAuthFromEnv(unittest.TestCase):
    def setUp(self):
        self.token_var_name = gitlab_api.AuthType.GITLAB_TOKEN.name
        self.oauth_var_name = gitlab_api.AuthType.GITLAB_OAUTH.name
        os.environ.pop(self.token_var_name, None)
        os.environ.pop(self.oauth_var_name, None)

    def test_token_set(self):
        token_value = 'my_token'
        os.environ[self.token_var_name] = token_value

        auth_type, auth_value = gitlab_api.auth_from_env()

        self.assertEqual(auth_type, gitlab_api.AuthType.GITLAB_TOKEN)
        self.assertEqual(auth_value, token_value)

    def test_oauth_set(self):
        oauth_value = 'my_oauth_token'
        os.environ[self.oauth_var_name] = oauth_value

        auth_type, auth_value = gitlab_api.auth_from_env()

        self.assertEqual(auth_type, gitlab_api.AuthType.GITLAB_OAUTH)
        self.assertEqual(auth_value, oauth_value)

    def test_both_set(self):
        token_value = 'my_token'
        oauth_value = 'my_oauth_token'
        os.environ[self.token_var_name] = token_value
        os.environ[self.oauth_var_name] = oauth_value

        auth_type, auth_value = gitlab_api.auth_from_env()

        self.assertEqual(auth_type, gitlab_api.AuthType.GITLAB_TOKEN)
        self.assertEqual(auth_value, token_value)

    def test_none_set(self):
        with self.assertRaises(ValueError):
            auth_type, auth_value = gitlab_api.auth_from_env()
