from setuptools import setup, find_packages
from setuptools.config.expand import entry_points

setup(
    name="portakal",
    version="0.0.3",
    packages=find_packages(),
    install_requires = [],
    entry_points={
        "console_scripts":"portakal-merhaba = portakal:hello"
    }
)