# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starknet_devnet',
 'starknet_devnet.blueprints',
 'starknet_devnet.blueprints.rpc',
 'starknet_devnet.blueprints.rpc.structures']

package_data = \
{'': ['*'],
 'starknet_devnet': ['accounts_artifacts/OpenZeppelin/0.5.1/Account.cairo/*']}

install_requires = \
['Flask[async]>=2.0.3,<2.1.0',
 'Werkzeug>=2.0.3,<2.1.0',
 'cairo-lang==0.12.2',
 'cloudpickle>=2.1.0,<2.2.0',
 'crypto-cpp-py>=1.4.0,<1.5.0',
 'flask-cors>=3.0.10,<3.1.0',
 'gunicorn>=20.1.0,<20.2.0',
 'jsonschema>=4.17.0,<4.18.0',
 'marshmallow-dataclass>=8.4,<8.5',
 'marshmallow>=3.17.0,<3.18.0',
 'poseidon-py>=0.1.3,<0.2.0',
 'pyyaml>=6.0.1,<6.1.0',
 'typing-extensions>=4.3.0,<4.4.0',
 'web3>=6.0.0,<6.1.0']

entry_points = \
{'console_scripts': ['starknet-devnet = starknet_devnet.server:deprecate']}

setup_kwargs = {
    'name': 'starknet-devnet',
    'version': '0.6.5',
    'description': 'A local testnet for Starknet',
    'long_description': '<!-- logo / title -->\n<p align="center" style="margin-bottom: 0px !important">\n  <img width="200" src="https://user-images.githubusercontent.com/2848732/193076972-da6fa36e-11f7-4cb3-aa29-673224f8576d.png" alt="Devnet" align="center">\n</p>\n<h1 align="center" style="margin-top: 0px !important">Starknet Devnet</h1>\n\n## ❗ Migrating to Rust\n\nThis repository (Devnet in Python) is not maintained anymore, so you are advised to switch to [Devnet in Rust](https://github.com/0xSpaceShard/starknet-devnet-rs), which aims to continue where Devnet in Python left off, but without the sequencer/gateway API.\n',
    'author': 'FabijanC',
    'author_email': 'fabijan.corak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/0xSpaceShard/starknet-devnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
