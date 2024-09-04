# setup.py

from setuptools import setup, find_packages

setup(
    name='networking-equinix',
    version='0.1',
    description='Neutron plugin for Equinix Metal integration',
    packages=find_packages(),
    entry_points={
        'neutron.core_plugins': [
            'equinix = networking_equinix.plugins.equinix_plugin:EquinixPlugin',
        ],
    },
    install_requires=[
        'requests',
        'oslo.config',
        'oslo.log',
        # Add other dependencies
    ],
)
