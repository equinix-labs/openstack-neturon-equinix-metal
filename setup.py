import setuptools

setuptools.setup(
    name='networking-equinix',
    version='0.1',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.20',
        'oslo.log>=3.36.0',
        'oslo.utils>=3.36.0',
        'six>=1.10.0'
    ],
    entry_points={
        'neutron.ml2.mechanism_drivers': [
            'equinix = networking_equinix.plugins.equinix_plugin:EquinixPlugin'
        ]
    }
)