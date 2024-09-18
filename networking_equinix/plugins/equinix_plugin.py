from neutron_lib.plugins import directory
from neutron_lib.plugins.ml2 import api
from oslo_config import cfg
from oslo_log import log as logging
from neutron.db import db_base_plugin_v2  # Needed for DB handling in Neutron
from neutron_lib import exceptions as n_exc  # Import Neutron exceptions
from networking_equinix.drivers.equinix_driver import EquinixDriver
import os

LOG = logging.getLogger(__name__)

# Register the configuration options for ml2_equinix
ml2_equinix_opts = [
    cfg.StrOpt('host', help="Equinix API host"),
    cfg.StrOpt('api_token', secret=True, help="API token for Equinix Metal"),
    cfg.StrOpt('project_id', help="Equinix Metal Project ID")
]

# Register the options under the 'ml2_equinix' group
cfg.CONF.register_opts(ml2_equinix_opts, 'ml2_equinix')

# Inherit both NeutronDbPluginV2 and api.MechanismDriver
class EquinixPlugin(db_base_plugin_v2.NeutronDbPluginV2, api.MechanismDriver):
    def __init__(self):
        LOG.info('Equinix Metal Plugin initialized with host: %s, project: %s', cfg.CONF.ml2_equinix, cfg.CONF.ml2_equinix)
        # print("Host:", CONF.ml2_equinix.hostt)
        # print("API Token:", CONF.ml2_equinix.api_token)
        # print("Project ID:", CONF.ml2_equinix.project_id)

        print("vasu:CONF.Object: %s", cfg.CONF.ml2_equinix)

        host = cfg.CONF.ml2_equinix.host
        api_token = cfg.CONF.ml2_equinix.api_token
        project_id = cfg.CONF.ml2_equinix.project_id

        # Initialize the Equinix driver
        self.driver = EquinixDriver(
            host=host,
            api_token=api_token,
            project_id=project_id
        )
        
        LOG.info('Equinix Metal Plugin initialized with host: %s, project: %s', host, project_id)

    def initialize(self):
        """
        Initialize the plugin and its configuration.
        """
        LOG.info('Initializing Equinix Metal Neutron Plugin')
        directory.add_plugin('equinix', self)

    def create_network_postcommit(self, context):
        """
        Called when a new network is created.
        """
        network = context.current
        LOG.info('Creating network: %s', network)

        vlan_data = {
            'vxlan': network.get('provider:segmentation_id'),  # VXLAN ID
            'description': network['name'],  # Network name
            'metro': network.get('metro', 'da')  # Default to 'da' if not provided
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

    def create_subnet_postcommit(self, context):
        """
        Called when a new subnet is created.
        """
        subnet = context.current
        network_id = subnet.get('network_id')
        cidr = subnet.get('cidr')
        gateway_ip = subnet.get('gateway_ip')
        subnet_name = subnet.get('name', 'Default Subnet')

        LOG.info('Creating subnet: %s with CIDR: %s and Gateway: %s', subnet_name, cidr, gateway_ip)

        # Equinix Metal API data for subnet creation
        subnet_data = {
            "type": "public_ipv4",
            "quantity": 4,  # Modify as needed
            "metro": "da",  # Modify as needed
            "fail_on_approval_required": "false"
        }

        try:
            # Call the Equinix Metal API to create the subnet
            response = self.driver.create_subnet(subnet_data)
            LOG.info('Successfully created subnet in Equinix Metal: %s', response)
        except Exception as e:
            LOG.error('Failed to create subnet in Equinix Metal: %s', e)
            raise n_exc.NeutronException("Failed to create Equinix subnet: %s" % str(e))

    def delete_subnet_postcommit(self, context):
        """
        Called when a subnet is deleted.
        """
        subnet = context.current
        subnet_id = subnet.get('id')

        LOG.info('Deleting subnet: %s', subnet_id)

        try:
            # Call the Equinix Metal API to delete the subnet
            self.driver.delete_subnet(subnet_id)
            LOG.info('Successfully deleted subnet in Equinix Metal')
        except Exception as e:
            LOG.error('Failed to delete subnet in Equinix Metal: %s', e)
            raise n_exc.NeutronException("Failed to delete Equinix subnet: %s" % str(e))