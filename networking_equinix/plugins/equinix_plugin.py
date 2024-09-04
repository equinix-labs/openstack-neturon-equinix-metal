# networking_equinix/plugins/equinix_plugin.py

from neutron_lib.plugins import directory
from neutron_lib.plugins.ml2 import api
from oslo_config import cfg
from oslo_log import log as logging

from networking_equinix.drivers.equinix_driver import EquinixDriver

LOG = logging.getLogger(__name__)

class EquinixPlugin(api.MechanismDriver):
    """
    Neutron service plugin for managing Equinix Metal resources.
    """

    def __init__(self):
        super(EquinixPlugin, self).__init__()
        self.host = cfg.CONF.EQUINIX.host
        self.api_token = cfg.CONF.EQUINIX.api_token
        self.driver = EquinixDriver(self.host, self.api_token)
        LOG.info('Equinix Metal Plugin initialized with host: %s', self.host)

    def initialize(self):
        # Initialize the plugin and its configuration
        LOG.info('Initializing Equinix Metal Neutron Plugin')
        directory.add_plugin('equinix', self)

    def create_network(self, context, network):
        # Logic for network creation using Equinix API
        LOG.info('Creating network: %s', network)
        project_id = network['project_id']
        vlan_data = {'description': network['name'], 'vxlan': network['vxlan']}
        self.driver.create_vlan(project_id, vlan_data)
        # Additional processing as required
