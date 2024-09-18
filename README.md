# Networking Equinix Plugin

## Overview

The `networking-equinix` plugin integrates OpenStack Neutron with [Equinix Metal](https://metal.equinix.com/), enabling management of network resources such as IP address ranges and VLANs directly through OpenStack.

## Features

- Create and manage IP address ranges on Equinix Metal
- Create and manage VLANs on Equinix Metal

## Requirements

- OpenStack Neutron
- Python 3.6 or above

## Installation

To install the `networking-equinix` plugin, enable it in your DevStack environment.

1. Add the following line to your `local.conf` file:

    ```bash
    enable_plugin networking-equinix https://github.com/codinja1188/networking-equinix.git
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

2. Run `stack.sh` to deploy OpenStack with the `networking-equinix` plugin enabled.
