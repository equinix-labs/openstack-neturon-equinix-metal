# networking_equinix/drivers/equinix_driver.py

from networking_equinix.api_client.equinix_api_client import EquinixAPIClient
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

class EquinixDriver:
    """
    Driver for managing Equinix Metal resources.
    """

    def __init__(self, host, api_token):
        self.api_client = EquinixAPIClient(host, api_token)

    def create_ip_range(self, project_id, ip_data):
        """
        Create an IP address range in a specified Equinix Metal project.

        :param project_id: The ID of the Equinix Metal project
        :param ip_data: Data for creating the IP address range
        :return: Response from the API call
        """
        LOG.info('Creating IP range in project %s', project_id)
        endpoint = f'/metal/v1/projects/{project_id}/ips'
        return self.api_client.execute(endpoint, method='POST', data=ip_data)

    def create_vlan(self, project_id, vlan_data):
        """
        Create a VLAN in a specified Equinix Metal project.

        :param project_id: The ID of the Equinix Metal project
        :param vlan_data: Data for creating the VLAN
        :return: Response from the API call
        """
        LOG.info('Creating VLAN in project %s', project_id)
        endpoint = f'/metal/v1/projects/{project_id}/vlans'
        return self.api_client.execute(endpoint, method='POST', data=vlan_data)
