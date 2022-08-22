from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='cyberfly-data-shipper',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'paho-mqtt',
        'pypact-lang'
    ],
    url='https://github.com/cyberfly-io/data-shipper',
    long_description=long_description,
    long_description_content_type='text/markdown'
)