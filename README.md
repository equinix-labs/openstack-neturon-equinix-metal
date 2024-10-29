# OpenStack Neutron Equinix Metal Plugin

## Overview

The `openstack-neutron-equinix-metal` plugin demonstrates how to integrate OpenStack Neutron with [Equinix Metal](https://deploy.equinix.com/product/bare-metal/), enabling management of network resources such as VLANs directly through OpenStack.

This project is intended for illustrative purposes in support of OpenStack Neutron plugin development.

## Features

- Create and manage IP address ranges on Equinix Metal VLANs through OpenStack Neutron
- Create and manage VLANs on Equinix Metal through Equinix Metal APIs

## Requirements

- [DevStack](https://docs.openstack.org/devstack/latest/)
- OpenStack Neutron
- Python 3.6 or above

## Installation

To install the `openstack-neutron-equinix-metal` [OpenStack/DevStack plugin](https://docs.openstack.org/devstack/latest/plugins.html), enable it in your [DevStack environment](https://docs.openstack.org/devstack/latest/).

1. Add the following line to your `local.conf` file:

    ```bash
    enable_plugin openstack-neutron-equinix-metal https://github.com/equinix-labs/openstack-neutron-equinix-metal.git
    ```

    ```bash
    [[post-config|$NEUTRON_CONF]]
    [DEFAULT]
    debug = True
    verbose = True

    [[post-config|$NEUTRON_CONF]]
    [ml2_equinix]
    host = api.equinix.com
    api_token = xxxxxxxxxxxxxxxxxxxx
    project_id = xxxx-xxxx-xxxx-xxxx-xxxx

    [[post-config|/$Q_PLUGIN_CONF_FILE]]
    [ml2]
    type_drivers=flat,gre,vlan,vxlan
    tenant_network_types=vxlan
    mechanism_drivers=equinix
    ```

2. Run `stack.sh` to deploy OpenStack with the `openstack-neutron-equinix-metal` plugin enabled.

## Usage

Once installed and configured, the plugin allows you to manage VLANs on Equinix Metal through OpenStack Neutron commands and the Horizon UI.

## Limitations

- Currently, the plugin supports only VLAN management (creation, deletion, and listing).
- Features such as Metal Gateway, VRF, and Interconnection are not implemented and not planned.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the [GitHub repository](https://github.com/equinix-labs/openstack-neutron-equinix-metal).

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.