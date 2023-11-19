import unittest
from unittest.mock import Mock, patch

from classes.config import Config
from windows.ConfigWindow import ConfigWindow


class ConfigWindowTest(unittest.TestCase):
    def setUp(self):
        self.appconfig = Config('test/config.json')
        self.config_window = ConfigWindow(self.appconfig)

    def test_on_save_button_click_saves_config(self):
        self.config_window.client_id_input.get = Mock(return_value="test_client_id")
        self.config_window.client_secret_input.get = Mock(return_value="test_client_secret")
        self.config_window.user_agent_input.get = Mock(return_value="test_user_agent")
        self.config_window.interval_input.get = Mock(return_value="10")

        with patch.object(self.appconfig, 'save_string') as mock_save_string, \
                patch.object(self.appconfig, 'set_int') as mock_set_int:
            self.config_window.on_save_button_click()

        mock_save_string.assert_any_call("client_id", "test_client_id")
        mock_save_string.assert_any_call("client_secret", "test_client_secret")
        mock_save_string.assert_any_call("user_agent", "test_user_agent")
        mock_set_int.assert_called_once_with("cooldown", "10")

    def test_on_connect_button_click_with_empty_fields(self):
        self.config_window.client_id_input.get = Mock(return_value="")
        self.config_window.client_secret_input.get = Mock(return_value="")
        self.config_window.user_agent_input.get = Mock(return_value="")

        with patch('builtins.print') as mock_print:
            self.config_window.on_connect_button_click()

        mock_print.assert_any_call("No client id entered")
        mock_print.assert_any_call("No client secret entered")
        mock_print.assert_any_call("No user agent entered")

    def test_on_connect_button_click_with_filled_fields(self):
        self.config_window.client_id_input.get = Mock(return_value="test_client_id")
        self.config_window.client_secret_input.get = Mock(return_value="test_client_secret")
        self.config_window.user_agent_input.get = Mock(return_value="test_user_agent")

        with patch.object(self.appconfig, 'save_string') as mock_save_string, \
                patch('classes.reddit.Reddit.get_refresh_token') as mock_get_refresh_token:
            mock_get_refresh_token.return_value = "test_refresh_token"
            self.config_window.on_connect_button_click()

        mock_save_string.assert_any_call("client_id", "test_client_id")
        mock_save_string.assert_any_call("client_secret", "test_client_secret")
        mock_save_string.assert_any_call("user_agent", "test_user_agent")
        mock_save_string.assert_any_call("refresh_token", "test_refresh_token")

    def test_checkbox_auto_remove_toggles_config(self):
        with patch.object(self.appconfig, 'toggle') as mock_toggle:
            self.config_window.checkbox_auto_remove()

        mock_toggle.assert_called_once_with("auto_remove")

    def test_get_refresh_token_status_when_token_exists(self):
        self.appconfig.get_key = Mock(return_value="test_refresh_token")

        status = self.config_window.get_refresh_token_status()

        self.assertEqual(status, 'Yes')

    def test_get_refresh_token_status_when_token_does_not_exist(self):
        self.appconfig.get_key = Mock(return_value="")

        status = self.config_window.get_refresh_token_status()

        self.assertEqual(status, 'No, click connect to connect')


if __name__ == '__main__':
    unittest.main()
