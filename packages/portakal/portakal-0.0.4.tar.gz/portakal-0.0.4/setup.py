from docutils.nodes import description
from setuptools import setup, find_packages
from setuptools.config.expand import entry_points

with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="portakal",
    version="0.0.4",
    packages=find_packages(),
    install_requires = [],
    entry_points={
        "console_scripts":"portakal-merhaba = portakal:hello"
    },
    long_description=long_description,
    long_description_content_type="text/markdown"
)