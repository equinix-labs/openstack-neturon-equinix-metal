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
        :return: Response from the API call or None if deletion is successful
        """
        LOG.info('Deleting VLAN with VXLAN ID: %s', vxlan_id)

        try:
            # Retrieve the list of VLANs to confirm the existence of the VXLAN
            existing_vlans = self.list_vlans()

            # Find the VLAN with the matching VXLAN ID
            matching_vlan = next((vlan for vlan in existing_vlans['virtual_networks'] if vlan['vxlan'] == vxlan_id), None)
            
            if not matching_vlan:
                LOG.warning('VLAN with VXLAN ID %s not found, skipping deletion', vxlan_id)
                return None  # No VLAN found, skip deletion

            vlan_id = matching_vlan['id']
            LOG.info('Found VLAN ID %s for VXLAN %s', vlan_id, vxlan_id)

        except Exception as e:
            LOG.error('Failed to list VLANs before deletion: %s', str(e))
            raise

        # Proceed to delete the VLAN using its ID
        endpoint = f'/metal/v1/virtual-networks/{vlan_id}'
        
        try:
            response = self.api_client.execute(endpoint, method='DELETE')

            # Handle 204 No Content response as successful deletion
            if response is None:  # A 204 No Content response will return None
                LOG.info("Successfully deleted VLAN with VXLAN: %s and ID: %s", vxlan_id, vlan_id)
                return None  # Successfully deleted with no content
            else:
                LOG.error("Unexpected response while deleting VLAN: %s", response)
                raise Exception(f"Unexpected response: {response}")

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

    def create_vrf(self, vrf_data):
        """
        Create a VRF in Equinix Metal.
        
        :param vrf_data: Dictionary containing VRF details.
        :return: API response.
        """
        endpoint = f'/metal/v1/projects/{self.project_id}/vrfs'
        LOG.info("Creating VRF in Equinix Metal: %s", vrf_data)
        
        try:
            return self.api_client.execute(endpoint, method='POST', data=vrf_data)
        except Exception as e:
            LOG.error("Failed to create VRF: %s", str(e))
            raise

    def delete_vrf(self, vrf_id):
        """
        Delete a VRF in Equinix Metal.
        
        :param vrf_id: The ID of the VRF to delete.
        :return: API response.
        """
        endpoint = f'/metal/v1/vrfs/{vrf_id}'
        LOG.info("Deleting VRF with ID: %s", vrf_id)
        
        try:
            return self.api_client.execute(endpoint, method='DELETE')
        except Exception as e:
            LOG.error("Failed to delete VRF: %s", str(e))
            raise

    def create_metal_gateway(self, gw_data):
        """Create Metal Gateway in Equinix"""
        LOG.info("Creating Equinix Metal gateways in Equinix Metal: %s", gw_data)
        endpoint = f'/metal/v1/projects/{self.project_id}/metal-gateways'
        try:
            return self.api_client.execute(endpoint, method='POST', data=gw_data)
        except Exception as e:
            LOG.error("Failed to delete VRF: %s", str(e))
            raise

    def delete_metal_gateway(self, gateway_id):
        """Delete Metal Gateway in Equinix"""
        endpoint = f'metal/v1/metal-gateways/{self.project_id}'
        LOG.info("Deleting Equinix Metal gateways with ID: %s", gateway_id)
        
        try:
            return self.api_client.execute(endpoint, method='DELETE')
        except Exception as e:
            LOG.error("Failed to delete VRF: %s", str(e))
            raise

    def create_subnet(self, subnet_data):
        """
        Create IPv4 Addresses
        """
        LOG.info("Creating Equinix Metal IPv4 Addresses : %s", subnet_data)
        endpoint = f'/metal/v1/projects/{self.project_id}/ips'
        try:
            return self.api_client.execute(endpoint, method='POST', data=subnet_data)
        except Exception as e:
            LOG.error("Failed to delete VRF: %s", str(e))
            raise

    def delete_subnet(self, subnet_id):
        """
        Delete IPv4 Addresses
        """
        LOG.info("Deleting Equinix Metal IPv4 Addresses: %s", subnet_id)
        endpoint = f'/metal/v1/vrfs/{subnet_id}'
        try:
            return self.api_client.execute(endpoint, method='DELETE')
        except Exception as e:
            LOG.error("Failed to delete VRF: %s", str(e))
            raise