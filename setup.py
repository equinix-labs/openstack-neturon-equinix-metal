import setuptools

setuptools.setup(
    name='networking-equinix',
    version='0.2',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.20',
        'oslo.log>=3.36.0',
        'oslo.utils>=3.36.0',
        'six>=1.10.0',
        'oslo.config>=8.0.0',
        'oslo.serialization>=4.0.0',
        'oslo.db>=12.0.0'
    ],
    extras_require={
        'testing': [
            'stestr>=3.1.0',
            'pytest>=6.0.0',
            'tox>=3.20.0'
        ]
    },
    entry_points={
        'neutron.ml2.mechanism_drivers': [
            'equinix = networking_equinix.plugins.equinix_plugin:EquinixPlugin'
        ],
        'neutron.service_plugins': [
            'l3_router = networking_equinix.plugins.equinix_l3_plugin:EquinixL3RouterPlugin'
        ],
        'oslo.config.opts': [
            'equinix = networking_equinix.plugins.equinix_plugin:list_opts'
        ]
    }
)
