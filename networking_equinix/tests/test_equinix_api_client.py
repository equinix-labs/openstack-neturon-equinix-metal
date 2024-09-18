# networking_equinix/tests/test_equinix_api_client.py

import unittest
from unittest.mock import patch, Mock
from networking_equinix.api_client.equinix_api_client import EquinixAPIClient


class TestEquinixAPIClient(unittest.TestCase):

    @patch('networking_equinix.api_client.equinix_api_client.requests.Session')
    def test_execute_get_request(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {'result': 'success'}
        mock_response.status_code = 200
        mock_session.return_value.get.return_value = mock_response

        client = EquinixAPIClient(host='api.equinix.com', api_token='xHj2Hr1XGRDEAbtNXmtWfAecEQ6wajTD')
        response = client.execute(endpoint='/metal/v1/projects')

        self.assertEqual(response['result'], 'success')
        mock_session.return_value.get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
