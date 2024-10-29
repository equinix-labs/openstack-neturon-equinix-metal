# Networking Equinix Plugin

## Overview

The `openstack-neutron-equinix-metal` plugin demonstrates how to integrate OpenStack Neutron with [Equinix Metal](https://deploy.equinix.com/product/bare-metal/), enabling management of network resources such as IP address ranges and VLANs directly through OpenStack.

## Features

- Create and manage IP address ranges on Equinix Metal
- Create and manage VLANs on Equinix Metal

## Requirements

- OpenStack Neutron
- Python 3.6 or above

## Installation

To install the `openstack-neutron-equinix-metal` plugin, enable it in your DevStack environment.

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
