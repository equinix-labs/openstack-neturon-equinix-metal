# networking_equinix/api_client/equinix_api_client.py

import json
import requests
from requests import exceptions as requests_exc
from oslo_log import log as logging
from oslo_utils import excutils
from six.moves.urllib import parse

from networking_equinix.common import exceptions as equinix_exc

LOG = logging.getLogger(__name__)

class EquinixAPIClient:
    """
    Client for interacting with Equinix Metal API.
    """

    def __init__(self, host, api_token, verify=False, timeout=None):
        self.host = host
        self.api_token = api_token
        self.timeout = timeout
        self.url = self._make_url(host)
        self.session = requests.Session()
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['X-Auth-Token'] = api_token
        self.session.verify = verify

    @staticmethod
    def _make_url(host, scheme='https'):
        return parse.urlunsplit((scheme, host, '', '', ''))

    def execute(self, endpoint, method='GET', data=None, params=None):
        """
        Executes an API call to the Equinix Metal API.

        :param endpoint: API endpoint to call (e.g., '/metal/v1/projects')
        :param method: HTTP method to use ('GET', 'POST', etc.)
        :param data: Data to send in the request body (for POST, PUT, etc.)
        :param params: Query parameters to include in the request
        :return: JSON response from the API
        """
        url = self.url + endpoint

        LOG.info('Equinix API request to %s with data %s', url, json.dumps(data) if data else '{}')

        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method == 'POST':
                response = self.session.post(url, data=json.dumps(data), timeout=self.timeout)
            elif method == 'PUT':
                response = self.session.put(url, data=json.dumps(data), timeout=self.timeout)
            elif method == 'DELETE':
                response = self.session.delete(url, timeout=self.timeout)
            else:
                raise ValueError("Unsupported HTTP method")

        except (requests_exc.ConnectionError, requests_exc.ConnectTimeout, requests_exc.Timeout) as e:
            error = f"Error during Equinix API request: {str(e)}"
            LOG.warning(error)
            raise equinix_exc.EquinixRpcError(msg=error)
        except Exception as e:
            with excutils.save_and_reraise_exception():
                LOG.warning('Error during processing the Equinix API request: %s', e)
        
        if response.status_code != requests.codes.ok:
            msg = f'Error ({response.status_code} - {response.reason}) while executing the command'
            LOG.error(msg)
            raise equinix_exc.EquinixRpcError(msg=response.text)

        try:
            return response.json()
        except ValueError:
            msg = "Invalid JSON response from Equinix Metal API"
            LOG.info(msg)
            raise equinix_exc.EquinixRpcError(msg=msg)
