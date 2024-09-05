# networking_equinix/plugins/equinix_plugin.py

from neutron_lib.plugins import directory
from neutron_lib.plugins.ml2 import api
from oslo_config import cfg
from oslo_log import log as logging
from oslo_config import cfg

from neutron.db import segments_db

from networking_equinix.drivers.equinix_driver import EquinixDriver
import os

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
CONF(default_config_files=['/etc/networking_equinix.conf'])

class EquinixPlugin(api.MechanismDriver):
    """
    Neutron mechanism driver for managing Equinix Metal resources.
    """
    def __init__(self, host, api_token=None, project_id=None):

        host = CONF.DEFAULT.host
        api_token = CONF.DEFAULT.api_token
        project_id = CONF.DEFAULT.project_id

        if not api_token or not host or not project_id:
            raise ValueError("API token, host, and project ID must be set either as parameters")
        
        LOG.info('Equinix Metal Plugin initialized with host: %s', self.host)

    def initialize(self):
        # Initialize the plugin and its configuration
        LOG.info('Initializing Equinix Metal Neutron Plugin')
        self.driver = EquinixDriver(self.host, self.api_token, self.project_id)
        directory.add_plugin('equinix', self)

    # def create_network(self, network_data):
    #     """
    #     Create a network in Equinix Metal.

    #     :param project_id: Equinix Metal project ID
    #     :param network_data: Details of the network to create
    #     :return: API response
    #     """
    #     try:
    #         LOG.info("Creating network with data: %s", network_data)
    #         return self.driver.create_vlan(network_data)
    #     except Exception as e:
    #         LOG.error("Failed to create network: %s", str(e))
    #         raise

    # def delete_network(self, vlan_id):
    #     """
    #     Delete a network in Equinix Metal.

    #     :param vlan_id: VLAN ID to delete
    #     :return: API response
    #     """
    #     try:
    #         LOG.info("Deleting network with VLAN ID: %s", vlan_id)
    #         return self.driver.delete_vlan(vlan_id)
    #     except Exception as e:
    #         LOG.error("Failed to delete network: %s", str(e))
    #         raise

    def create_network_postcommit(self, context):
        """
        Called when a new network is created.
        """
        network = context.current
        LOG.info('Creating network: %s', network)
        # vlan_data = {
        #     'vxlan': network.get('provider:segmentation_id'),  # Ensure this is an integer
        #     'description': network['name'],  # Ensure this is a string
        #     'metro': network.get('metro', '<default_metro>')  # Replace <default_metro> with a default value if needed
        # }
        vlan_data = {
            'vxlan': '1000',  # Ensure this is an integer
            'description': 'test1000',  # Ensure this is a string
            'metro': 'da'  # Replace <default_metro> with a default value if needed
        }
        try:
            self.driver.create_vlan(vlan_data)
        except Exception as e:
            LOG.error('Failed to create network in Equinix: %s', e)
            raise

    def delete_network_postcommit(self, context):
        """
        Called when a network is deleted.
        """
        network = context.current
        LOG.info('Deleting network: %s', network)
        vlan_id = network.get('provider:segmentation_id')
        try:
            self.driver.delete_vlan(vlan_id)
        except Exception as e:
            LOG.error('Failed to delete network in Equinix: %s', e)
            raise

    def create_port_postcommit(self, context):
        """
        Called when a new port is created.
        """
        port = context.current
        LOG.info('Creating port: %s', port)
        # TODO: Implement logic for creating ports using the Equinix API.

    def delete_port_postcommit(self, context):
        """
        Called when a port is deleted.
        """
        port = context.current
        LOG.info('Deleting port: %s', port)
        # TODO: Implement logic for deleting ports using the Equinix API.

    def create_subnet_postcommit(self, context):
        """
        Called when a new subnet is created.
        """
        subnet = context.current
        LOG.info('Creating subnet: %s', subnet)
        # TODO: Implement logic for creating subnets using the Equinix API.

    def delete_subnet_postcommit(self, context):
        """
        Called when a subnet is deleted.
        """
        subnet = context.current
        LOG.info('Deleting subnet: %s', subnet)
        # TODO: Implement logic for deleting subnets using the Equinix API.

    # Additional methods can be defined here as required.
