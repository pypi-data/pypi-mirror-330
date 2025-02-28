# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certificate_cli']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=3.0.3,<4.0.0',
 'cryptography>=43.0.0,<44.0.0',
 'typer[all]>=0.12.4,<0.13.0']

entry_points = \
{'console_scripts': ['certificate_cli = certificate_cli.main:start_cli']}

setup_kwargs = {
    'name': 'certificate-cli',
    'version': '0.2.3',
    'description': '',
    'long_description': '# `certificate_cli`\n\n**Usage**:\n\n```console\n$ certificate_cli [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `generate`: Generate a SSL certificate\n* `info`: Basic info of a pem certificate\n* `simulate`: Provide a path to public and private...\n\n## `certificate_cli generate`\n\nGenerate a SSL certificate\n\n**Usage**:\n\n```console\n$ certificate_cli generate [OPTIONS]\n```\n\n**Options**:\n\n* `--days INTEGER`: [default: 30]\n* `--prefix TEXT`\n* `--path TEXT`: [default: ./certs]\n* `--help`: Show this message and exit.\n\n## `certificate_cli info`\n\nBasic info of a pem certificate\n\n**Usage**:\n\n```console\n$ certificate_cli info [OPTIONS] PATH\n```\n\n**Arguments**:\n\n* `PATH`: [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `certificate_cli simulate`\n\nProvide a path to public and private certificates.\n\nUse --port to specify a port to serve the certificat on.\n\n**Usage**:\n\n```console\n$ certificate_cli simulate [OPTIONS] PUBLIC PRIVATE\n```\n\n**Arguments**:\n\n* `PUBLIC`: [required]\n* `PRIVATE`: [required]\n\n**Options**:\n\n* `--port INTEGER`: [default: 5678]\n* `--help`: Show this message and exit.\n\n## Build\n\n1. Increment versions in `__init.py__` and `pyproject.toml`\n2. Update changelog (`git log --pretty=format:"%h - %s (%an, %ad)" --date=short` for starters, also see [git-chglog](https://github.com/git-chglog/git-chglog)).\n3. `build` and `publish`\n\n```\npoetry build\npoetry publish\nor \npoetry publish --build',
    'author': 'Ben Davidson',
    'author_email': 'ben.davidson@dynatrace.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
