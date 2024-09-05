from networking_equinix.api_client.equinix_api_client import EquinixAPIClient
from oslo_log import log as logging
import os

LOG = logging.getLogger(__name__)

class EquinixDriver:
    """
    Driver for managing Equinix Metal resources.
    """
    def __init__(self, host=None, api_token=None, project_id=None):
        # Fetch configuration from file if not provided
        self.api_client = EquinixAPIClient(host, api_token)
        self.timeout = 30

    def create_vlan(self, vlan_data):
        """
        Create a VLAN in a specified Equinix Metal project.

        :param vlan_data: A dictionary containing VLAN details (e.g., description, vxlan)
        :return: Response from the API call
        """
        LOG.info('Creating VLAN in project %s with data: %s', self.project_id, vlan_data)
        endpoint = f'/metal/v1/projects/{self.project_id}/vlans'
        try:
            return self.api_client.execute(endpoint, method='POST', data=vlan_data)
        except Exception as e:
            LOG.error("Failed to create VLAN: %s", str(e))
            raise

    def delete_vlan(self, vlan_id):
        """
        Delete a VLAN in a specified Equinix Metal project.

        :param vlan_id: The ID of the VLAN to delete
        :return: Response from the API call
        """
        LOG.info('Deleting VLAN with ID: %s', vlan_id)
        endpoint = f'/metal/v1/vlans/{vlan_id}'
        try:
            return self.api_client.execute(endpoint, method='DELETE')
        except Exception as e:
            LOG.error("Failed to delete VLAN: %s", str(e))
            raise

    def list_vlans(self, project_id):
        """
        List VLANs in a specified Equinix Metal project.

        :param project_id: The ID of the Equinix Metal project
        :return: Response from the API call
        """
        LOG.info('Listing VLANs for project %s', project_id)
        endpoint = f'/metal/v1/projects/{project_id}/vlans'
        return self.api_client.execute(endpoint, method='GET')

    def create_device(self, project_id, device_data):
        """
        Create a device in a specified Equinix Metal project.

        :param project_id: The ID of the Equinix Metal project
        :param device_data: Data for creating the device
        :return: Response from the API call
        """
        LOG.info('Creating device in project %s', project_id)
        endpoint = f'/metal/v1/projects/{project_id}/devices'
        return self.api_client.execute(endpoint, method='POST', data=device_data)

    def delete_device(self, device_id):
        """
        Delete a device in a specified Equinix Metal project.

        :param device_id: The ID of the device to delete
        :return: Response from the API call
        """
        LOG.info('Deleting device with ID %s', device_id)
        endpoint = f'/metal/v1/devices/{device_id}'
        return self.api_client.execute(endpoint, method='DELETE')

    def list_devices(self, project_id):
        """
        List devices in a specified Equinix Metal project.

        :param project_id: The ID of the Equinix Metal project
        :return: Response from the API call
        """
        LOG.info('Listing devices for project %s', project_id)
        endpoint = f'/metal/v1/projects/{project_id}/devices'
        return self.api_client.execute(endpoint, method='GET')

    def create_bgp_session(self, device_id, session_data):
        """
        Create a BGP session for a device.

        :param device_id: The ID of the device
        :param session_data: Data for creating the BGP session
        :return: Response from the API call
        """
        LOG.info('Creating BGP session for device %s', device_id)
        endpoint = f'/metal/v1/devices/{device_id}/bgp/sessions'
        return self.api_client.execute(endpoint, method='POST', data=session_data)

    def delete_bgp_session(self, session_id):
        """
        Delete a BGP session.

        :param session_id: The ID of the BGP session to delete
        :return: Response from the API call
        """
        LOG.info('Deleting BGP session with ID %s', session_id)
        endpoint = f'/metal/v1/bgp/sessions/{session_id}'
        return self.api_client.execute(endpoint, method='DELETE')

    def list_bgp_sessions(self, device_id):
        """
        List BGP sessions for a device.

        :param device_id: The ID of the device
        :return: Response from the API call
        """
        LOG.info('Listing BGP sessions for device %s', device_id)
        endpoint = f'/metal/v1/devices/{device_id}/bgp/sessions'
        return self.api_client.execute(endpoint, method='GET')

    def list_ip_addresses(self, project_id):
        """
        List IP addresses in a specified Equinix Metal project.

        :param project_id: The ID of the Equinix Metal project
        :return: Response from the API call
        """
        LOG.info('Listing IP addresses for project %s', project_id)
        endpoint = f'/metal/v1/projects/{project_id}/ips'
        return self.api_client.execute(endpoint, method='GET')

    def delete_ip_range(self, ip_range_id):
        """
        Delete an IP range in a specified Equinix Metal project.

        :param ip_range_id: The ID of the IP range to delete
        :return: Response from the API call
        """
        LOG.info('Deleting IP range with ID %s', ip_range_id)
        endpoint = f'/metal/v1/ips/{ip_range_id}'
        return self.api_client.execute(endpoint, method='DELETE')
