from neutron.db import segments_db

from networking_equinix.drivers.equinix_driver import EquinixDriver
import os

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

class EquinixPlugin(api.MechanismDriver):
    """
    Neutron mechanism driver for managing Equinix Metal resources.
    """
    def __init__(self):
        CONF(default_config_files=['/etc/networking-equinix/networking_equinix.conf'])
        host = CONF.DEFAULT.host
        api_token = CONF.DEFAULT.api_token
        project_id = CONF.DEFAULT.project_id

        if not api_token or not host or not project_id:
            raise ValueError("API token, host, and project ID must be set either as parameters")

        # Initialize the driver with the required parameters
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