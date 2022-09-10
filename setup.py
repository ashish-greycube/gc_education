from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in gc_education/__init__.py
from gc_education import __version__ as version

setup(
	name="gc_education",
	version=version,
	description="Education Module Extensions",
	author="Greycube",
	author_email="admin@greycube.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
