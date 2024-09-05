# networking-equinix/devstack/plugin.sh

# Define the directory where the networking-equinix plugin is located
NETWORKING_EQUINIX_DIR=/opt/stack/networking-equinix

function install_networking_equinix {
    echo "Installing Equinix Metal Neutron Plugin"
    # Use setup_develop to install the plugin in editable mode from the correct directory
    setup_develop $NETWORKING_EQUINIX_DIR
}

function configure_networking_equinix {
    echo "Configuring Equinix Metal Neutron Plugin"
    iniset $NEUTRON_CONF DEFAULT core_plugin neutron.plugins.ml2.plugin.Ml2Plugin
    iniset $NEUTRON_CONF DEFAULT service_plugins networking_equinix.plugins.equinix_plugin.EquinixPlugin

    # Define the source and destination for the configuration file
    local src_conf_file=$NETWORKING_EQUINIX_DIR/etc/networking_equinix.conf
    local dest_conf_dir=/etc/networking-equinix/
    local dest_conf_file=$dest_conf_dir/networking_equinix.conf

    # Create the destination directory if it does not exist
    sudo mkdir -p $dest_conf_dir

    # Copy the configuration file to the destination
    sudo cp $src_conf_file $dest_conf_file

    echo "Copied configuration file to $dest_conf_file"
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
