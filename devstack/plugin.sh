# networking_equinix/devstack/plugin.sh

function install_networking_equinix {
    echo "Installing Equinix Metal Neutron Plugin"
    setup_develop $NETWORKING_EQUINIX_DIR
}

function configure_networking_equinix {
    echo "Configuring Equinix Metal Neutron Plugin"
    iniset $NEUTRON_CONF DEFAULT core_plugin neutron.plugins.ml2.plugin.Ml2Plugin
    iniset $NEUTRON_CONF DEFAULT service_plugins networking_equinix.plugins.equinix_plugin.EquinixPlugin
}

if is_service_enabled q-svc; then
    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing Equinix Metal Neutron Plugin"
        install_networking_equinix
    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring Equinix Metal Neutron Plugin"
        configure_networking_equinix
    fi
fi
