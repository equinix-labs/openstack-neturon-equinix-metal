# Networking Equinix Plugin

## Overview

The `networking-equinix` plugin integrates OpenStack Neutron with [Equinix Metal](https://metal.equinix.com/), enabling management of network resources (such as IP address ranges and VLANs) directly through OpenStack.

## Features

- Create and manage IP address ranges on Equinix Metal
- Create and manage VLANs on Equinix Metal

## Requirements

- OpenStack Neutron
- Python 3.6 or above

## Installation

To install the `networking-equinix` plugin, you need to enable it in your DevStack environment.

1. Add the following line to your `local.conf` file:

    ```bash
    enable_plugin networking-equinix https://github.com/your-repo/networking-equinix.git
    ```

2. Run `stack.sh` to deploy OpenStack with the `networking-equinix` plugin enabled.

## Configuration

Configure the Equinix Metal API credentials in `neutron.conf` or `networking_equinix.conf`:

```ini
[equinix]
host = api.equinix.com
api_token = your_equinix_api_token
