import pathlib
from platform import python_version

from setuptools import setup,find_packages

setup(name="greeksoft",
      version='0.0.2',
      description="GreekSoft Api Client use for trading purpose",
      long_description=pathlib.Path("README.md").read_text(),
      long_description_content_type='text/markdown',
      author="Greek_dev_Team",
      author_email='greeksoftapi@greeksoft.co.in',
      license="MIT License",
      packages=find_packages(),
      install_requires=[
            'websocket>=0.2.1',
            'requests>=2.32.3',
            'pandas>=1.19.5',
            'websockets>=14.2',
            'websocket-client>=1.8.0'
      ],
      python_version="=>3.10",
      include_package_data=True,

      )