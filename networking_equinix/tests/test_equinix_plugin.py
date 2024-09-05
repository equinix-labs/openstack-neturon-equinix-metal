# networking_equinix/tests/test_equinix_plugin.py

import unittest
from unittest.mock import patch, Mock
from networking_equinix.plugins.equinix_plugin import EquinixPlugin


class TestEquinixPlugin(unittest.TestCase):

    @patch('networking_equinix.plugins.equinix_plugin.EquinixDriver')
    def test_create_network(self, mock_driver):
        mock_driver_instance = mock_driver.return_value
        plugin = EquinixPlugin()
        context = {}  # Replace with appropriate mock context
        network = {'project_id': '12345', 'name': 'test-network', 'vxlan': '1234'}

        plugin.create_network(context, network)

        mock_driver_instance.create_vlan.assert_called_once_with('12345', {'description': 'test-network', 'vxlan': '1234'})


if __name__ == '__main__':
    unittest.main()
