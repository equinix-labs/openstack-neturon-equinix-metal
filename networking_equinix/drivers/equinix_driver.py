from networking_equinix.api_client.equinix_api_client import EquinixAPIClient
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

class EquinixDriver:
    """
    Driver for managing Equinix Metal resources.
    """
    def __init__(self, host=None, api_token=None, project_id=None):
        # Initialize the API client with host and token, and store the project_id
        self.api_client = EquinixAPIClient(host, api_token)
        self.project_id = project_id
        self.timeout = 30

    def create_vlan(self, vlan_data):
        """
        Create a VLAN in a specified Equinix Metal project.

        :param vlan_data: A dictionary containing VLAN details (e.g., description, vxlan)
        :return: Response from the API call
        """
        LOG.info('Creating VLAN in project %s with data: %s', self.project_id, vlan_data)
        endpoint = f'/metal/v1/projects/{self.project_id}/virtual-networks'  # Changed to /virtual-networks
        try:
            return self.api_client.execute(endpoint, method='POST', data=vlan_data)
        except Exception as e:
            LOG.error("Failed to create VLAN: %s", str(e))
            raise

    def delete_vlan(self, vxlan_id):
        """
        Delete a VLAN in a specified Equinix Metal project using its VXLAN ID.

        :param vxlan_id: The VXLAN ID of the VLAN to delete
        :return: Response from the API call or None if deletion is skipped
        """
        LOG.info('Deleting VLAN with VXLAN ID: %s', vxlan_id)

        # Verify if the VLAN with the specified VXLAN exists before deletion
        try:
            existing_vlans = self.list_vlans()  # Assuming this method lists all VLANs

            # Check if the VXLAN exists in the list of VLANs and get the corresponding VLAN ID
            matching_vlan = next((vlan for vlan in existing_vlans['virtual_networks'] if vlan['vxlan'] == vxlan_id), None)

            if not matching_vlan:
                LOG.warning('VLAN with VXLAN ID %s not found, skipping deletion', vxlan_id)
                return None  # Skip deletion if VLAN with this VXLAN is not found

            # Extract the actual VLAN ID from the matching VLAN
            vlan_id = matching_vlan['id']
            LOG.info('Found VLAN ID %s for VXLAN %s', vlan_id, vxlan_id)

        except Exception as e:
            LOG.error('Failed to list VLANs before deletion: %s', str(e))
            raise

        # Proceed to delete the VLAN using the ID
        endpoint = f'/metal/v1/virtual-networks/{vlan_id}'
        try:
            response = self.api_client.execute(endpoint, method='DELETE')

            # Check for the HTTP 204 - No Content response, which indicates a successful deletion
            if response.status_code == 204:
                LOG.info("Successfully deleted VLAN with VXLAN: %s and ID: %s", vxlan_id, vlan_id)
                return response
            else:
                LOG.error("Unexpected response while deleting VLAN: %s", response.status_code)
                raise Exception(f"Unexpected response: {response.status_code}")

        except Exception as e:
            LOG.error("Failed to delete VLAN: %s", str(e))
            raise

    def list_vlans(self):
        """
        List VLANs in the specified Equinix Metal project.

        :return: Response from the API call
        """
        if not self.project_id:
            raise ValueError("Project ID must be set to list VLANs.")

        LOG.info('Listing VLANs for project %s', self.project_id)
        endpoint = f'/metal/v1/projects/{self.project_id}/virtual-networks'

        try:
            response = self.api_client.execute(endpoint, method='GET')
            if 'virtual_networks' not in response:
                LOG.error("Unexpected response format when listing VLANs: %s", response)
                raise ValueError("Expected a list of VLANs but received something else.")
            return response  # Expecting the response to have a 'virtual_networks' key with the list of VLANs
        except Exception as e:
            LOG.error("Failed to list VLANs: %s", str(e))
            raise


    # def create_device(self, project_id, device_data):
    #     """
    #     Create a device in a specified Equinix Metal project.

    #     :param project_id: The ID of the Equinix Metal project
    #     :param device_data: Data for creating the device
    #     :return: Response from the API call
    #     """
    #     LOG.info('Creating device in project %s', project_id)
    #     endpoint = f'/metal/v1/projects/{project_id}/devices'
    #     return self.api_client.execute(endpoint, method='POST', data=device_data)

    # def delete_device(self, device_id):
    #     """
    #     Delete a device in a specified Equinix Metal project.

    #     :param device_id: The ID of the device to delete
    #     :return: Response from the API call
    #     """
    #     LOG.info('Deleting device with ID %s', device_id)
    #     endpoint = f'/metal/v1/devices/{device_id}'
    #     return self.api_client.execute(endpoint, method='DELETE')

    # def list_devices(self, project_id):
    #     """
    #     List devices in a specified Equinix Metal project.

    #     :param project_id: The ID of the Equinix Metal project
    #     :return: Response from the API call
    #     """
    #     LOG.info('Listing devices for project %s', project_id)
    #     endpoint = f'/metal/v1/projects/{project_id}/devices'
    #     return self.api_client.execute(endpoint, method='GET')

    # def create_bgp_session(self, device_id, session_data):
    #     """
    #     Create a BGP session for a device.

    #     :param device_id: The ID of the device
    #     :param session_data: Data for creating the BGP session
    #     :return: Response from the API call
    #     """
    #     LOG.info('Creating BGP session for device %s', device_id)
    #     endpoint = f'/metal/v1/devices/{device_id}/bgp/sessions'
    #     return self.api_client.execute(endpoint, method='POST', data=session_data)

    # def delete_bgp_session(self, session_id):
    #     """
    #     Delete a BGP session.

    #     :param session_id: The ID of the BGP session to delete
    #     :return: Response from the API call
    #     """
    #     LOG.info('Deleting BGP session with ID %s', session_id)
    #     endpoint = f'/metal/v1/bgp/sessions/{session_id}'
    #     return self.api_client.execute(endpoint, method='DELETE')

    # def list_bgp_sessions(self, device_id):
    #     """
    #     List BGP sessions for a device.

    #     :param device_id: The ID of the device
    #     :return: Response from the API call
    #     """
    #     LOG.info('Listing BGP sessions for device %s', device_id)
    #     endpoint = f'/metal/v1/devices/{device_id}/bgp/sessions'
    #     return self.api_client.execute(endpoint, method='GET')

    # def list_ip_addresses(self, project_id):
    #     """
    #     List IP addresses in a specified Equinix Metal project.

    #     :param project_id: The ID of the Equinix Metal project
    #     :return: Response from the API call
    #     """
    #     LOG.info('Listing IP addresses for project %s', project_id)
    #     endpoint = f'/metal/v1/projects/{project_id}/ips'
    #     return self.api_client.execute(endpoint, method='GET')

    # def delete_ip_range(self, ip_range_id):
    #     """
    #     Delete an IP range in a specified Equinix Metal project.

    #     :param ip_range_id: The ID of the IP range to delete
    #     :return: Response from the API call
    #     """
    #     LOG.info('Deleting IP range with ID %s', ip_range_id)
    #     endpoint = f'/metal/v1/ips/{ip_range_id}'
    #     return self.api_client.execute(endpoint, method='DELETE')
