# networking_equinix/tests/test_equinix_plugin.py

import unittest
from unittest.mock import patch, Mock
from networking_equinix.plugins.equinix_plugin import EquinixPlugin
from networking_equinix.api_client.equinix_api_client import EquinixAPIClient
class TestEquinixPlugin(unittest.TestCase):

    @patch('networking_equinix.plugins.equinix_plugin.EquinixDriver')
    @patch('networking_equinix.plugins.equinix_plugin.CONF')
    def test_create_network_postcommit(self, mock_conf, mock_driver):
        # Mock configuration values
        client = EquinixAPIClient(host='api.equinix.com', api_token='xHj2Hr1XGRDEAbtNXmtWfAecEQ6wajTD')
        mock_conf.host = 'api.equinix.com'
        mock_conf.api_token = 'xHj2Hr1XGRDEAbtNXmtWfAecEQ6wajTD'
        mock_conf.project_id = 'b834475b-deb7-4d89-b681-6feab1fced57'

        # Mock the EquinixDriver instance
        mock_driver_instance = mock_driver.return_value

        # Instantiate the plugin
        plugin = EquinixPlugin()

        # Mock the context object
        mock_context = Mock()
        mock_context.current = {
            'id': 'network_id',
            'project_id': '12345',
            'name': 'test-network',
            'provider:segmentation_id': 1234,  # VXLAN ID
            'metro': 'SV'
        }

        # Call the method to test
        plugin.create_network_postcommit(mock_context)

        # Assert that create_vlan was called with correct arguments
        mock_driver_instance.create_vlan.assert_called_once_with({
            'vxlan': 1234,
            'description': 'test-network',
            'metro': 'SV'
        })

if __name__ == '__main__':
    unittest.main()

