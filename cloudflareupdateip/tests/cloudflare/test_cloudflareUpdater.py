import unittest
from unittest.mock import patch, MagicMock
from cloudflareupdateip.application.runner import CloudflareUpdater


class TestCloudflareUpdater(unittest.TestCase):

    @patch('cloudflareupdateip.application.runner.cloudflare_api')
    @patch('cloudflareupdateip.application.runner.get_my_current_public_ip')
    @patch('os.environ.get')
    def test_update_when_value_has_changed(self, mock_get, mock_get_ip, mock_cf_api):
        # Arrange
        def side_effect(arg, default=None):
            if arg == 'CF_TOKEN':
                return 'test_token'
            if arg == 'CURRENT_DOMAIN':
                return 'test.com'
            return default

        mock_get.side_effect = side_effect
        mock_get_ip.return_value = '123.123.123.124'
        mock_cf_api_instance = MagicMock()
        mock_cf_api.return_value = mock_cf_api_instance
        mock_cf_api_instance.get_current_a_record.return_value = '123.123.123.123'

        # Act
        updater = CloudflareUpdater()
        updater.update("123.123.123.124")

        # Assert
        mock_cf_api.assert_called_once_with('test_token')
        mock_cf_api_instance.get_current_a_record.assert_called_once_with('test.com')
        mock_cf_api_instance.update_the_a_record.assert_called_once_with('123.123.123.124', 'test.com')

    @patch('cloudflareupdateip.application.runner.cloudflare_api')
    @patch('cloudflareupdateip.application.runner.get_my_current_public_ip')
    @patch('os.environ.get')
    def test_do_not_update_when_the_current_ip_equals_A_record_value(self, mock_get, mock_get_ip, mock_cf_api):
        # Arrange
        def side_effect(arg, default=None):
            if arg == 'CF_TOKEN':
                return 'test_token'
            if arg == 'CURRENT_DOMAIN':
                return 'test.com'
            return default

        mock_get.side_effect = side_effect
        mock_get_ip.return_value = '123.123.123.123'
        mock_cf_api_instance = MagicMock()
        mock_cf_api.return_value = mock_cf_api_instance
        mock_cf_api_instance.get_current_a_record.return_value = '123.123.123.123'

        # Act
        updater = CloudflareUpdater()
        updater.update("123.123.123.123")

        # Assert
        mock_cf_api.assert_called_once_with('test_token')
        mock_cf_api_instance.get_current_a_record.assert_called_once_with('test.com')
        mock_cf_api_instance.update_the_a_record.assert_not_called()


if __name__ == '__main__':
    unittest.main()
