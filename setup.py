from setuptools import setup, find_packages
from tsuru_autoscale import __version__


setup(
    name="tsuru_autoscale",
    url="https://github.com/tsuru/tsuru-autoscale-dashboard",
    version=__version__,
    packages=find_packages(),
    description="Web dashboard for tsuru autoscale service",
    author="tsuru",
    author_email="tsuru@corp.globo.com",
    include_package_data=True,
    install_requires=[
        "Django>=1.10.2",
        "requests>=2.8.1",
    ],
)
