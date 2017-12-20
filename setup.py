# -*- coding: utf-8 -*-
# übernommen aus: https://pythonhosted.org/setuptools/setuptools.html#id24
import ez_setup
from CobraSync import __version__

ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
      name = "CobraSync",
      packages = find_packages(),
      version = __version__,
      # Abhängigkeiten
      install_requires = ["configobj==5.0.6", "cx-Oracle==5.1.3", "requests==2.8.0", "PyMySQL==0.7.4", "python-keyczar==0.715", "pymssql==2.1.3"],
      # PyPI metadata
      author = "Peter Schär",
      author_email = "peter.schaer@bve.be.ch",
      description = "Synchronisation aus der Cobra Adressdatenbank nach GeoDBmeta und GeoDBProzess",
      url = "http://www.be.ch/geoportal",
      entry_points={
           'console_scripts': [
                'CobraSync = CobraSync.helpers.commandline_helper:main'
            ]         
      }
      # https://pythonhosted.org/setuptools/setuptools.html#automatic-script-creation
)
