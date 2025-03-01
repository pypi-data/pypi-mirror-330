# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pincell_moment_utils', 'pincell_moment_utils.input_files']

package_data = \
{'': ['*'], 'pincell_moment_utils': ['data/*']}

install_requires = \
['matplotlib',
 'mpi4py',
 'numpy',
 'openmc',
 'pandas',
 'py7zr',
 'pyprojroot',
 'scipy',
 'shutil',
 'subprocess',
 'typing']

setup_kwargs = {
    'name': 'pincell-moment-utils',
    'version': '0.0.2',
    'description': 'A tool for postprocessing and calculating flux moments for a pincell model',
    'long_description': '# Introduction\nThis project primarily serves as a reference to the methods used to generate a moment dataset for parameterizing the incident and outgoing fluxes, as well as the local multiplication factor and the pin flux distribution for training a machine learning model to implement the incident flux response method. Included is also a utility package which was used to postprocess moment and mesh tallies and perform flux reconstruction from these moments following the theory described in `TODO`.\n\n# Installation and Setup\nThis package is [published on PyPI](https://pypi.org/project/pincell_moment_utils/), and so can be installed (along with all of the necessary dependencies) via `pip`\n```\npip install pincell_moment_utils\n```\nNote some of the features require the ability to run transport simulations with OpenMC, which require a valid set of cross sections, which can be installed using the scripts [here](https://github.com/openmc-dev/data).',
    'author': 'Matthew Louis',
    'author_email': 'matthewlouis31@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
