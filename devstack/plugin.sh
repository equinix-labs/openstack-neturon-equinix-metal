# openstack-neutron-equinix-metal/devstack/plugin.sh

# Define the directory where the openstack-neutron-equinix-metal plugin is located
NETWORKING_EQUINIX_DIR=/opt/stack/openstack-neutron-equinix-metal

function install_networking_equinix {
    echo "Installing Equinix Metal Neutron Plugin"
    # Use setup_develop to install the plugin in editable mode from the correct directory
    setup_develop $NETWORKING_EQUINIX_DIR
}

function configure_networking_equinix {
    echo "Configuring Equinix Metal Neutron Plugin"

    # Configure the core and service plugins
    iniset $NEUTRON_CONF DEFAULT core_plugin neutron.plugins.ml2.plugin.Ml2Plugin
    iniset $NEUTRON_CONF DEFAULT service_plugins networking_equinix.plugins.equinix_l3_plugin.EquinixL3RouterPlugin

    # Set up the ML2 mechanism drivers to include equinix
    iniset $NEUTRON_CONF ml2 mechanism_drivers equinix

}

function configure_l3_plugin {
    echo "Configuring L3 Router Service Plugin"

    # Add the L3 plugin and its configurations
    iniset $NEUTRON_CONF DEFAULT router_scheduler_driver neutron.scheduler.l3_agent_scheduler.ChanceScheduler

    # Set additional configurations for L3 plugin if needed
    iniset $NEUTRON_CONF l3 external_network_bridge ""
    iniset $NEUTRON_CONF l3 enable_metadata_proxy True

    echo "L3 Router Service Plugin configured successfully"
}

function start_services {
    echo "Starting Neutron Services"
    # Make sure to restart neutron services after installing and configuring the plugin
    sudo systemctl restart devstack@q-svc.service
    sudo systemctl restart devstack@q-l3.service
}

# Main logic to call functions based on the stage of the stack process
if is_service_enabled q-svc; then
    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing Equinix Metal Neutron Plugin"
        install_networking_equinix
    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring Equinix Metal Neutron Plugin"
        configure_networking_equinix
        configure_l3_plugin
    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        echo_summary "Starting Neutron Services"
        start_services
    fi
fi
