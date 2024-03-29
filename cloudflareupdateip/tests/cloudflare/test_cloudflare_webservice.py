from unittest.mock import patch, MagicMock
import pytest
from cloudflareupdateip.backend.model import cloudflare_api

def test_update_the_a_record():
    with patch('cloudflareupdateip.backend.model.CloudFlare.CloudFlare') as MockCloudFlare:
        # Create a MagicMock instance for the zones and dns_records attributes
        mock_zones = MagicMock()
        mock_dns_records = MagicMock()

        # Set the return values for the get and put methods
        mock_zones.get.return_value = [{'id': 'zone_id'}]
        mock_dns_records.get.return_value = [{'id': 'dns_record_id', 'name': 'test.com', 'type': 'A'}]

        # Set the zones and dns_records attributes of the CloudFlare instance
        MockCloudFlare.return_value.zones = mock_zones
        MockCloudFlare.return_value.zones.dns_records = mock_dns_records

        # Instantiate the cloudflare_api class
        cf_api = cloudflare_api('test_token')

        # Call the update_the_a_record function with a test IP address and domain
        cf_api.update_the_a_record('123.123.123.123', 'test.com')

        # Assert that the get and put methods were called with the correct arguments
        mock_zones.get.assert_called_once_with(params={'name': 'test.com'})
        mock_dns_records.get.assert_called_once_with('zone_id')
        mock_dns_records.put.assert_called_once_with('zone_id', 'dns_record_id', data={
            'name': 'test.com',
            'type': 'A',
            'content': '123.123.123.123'
        })