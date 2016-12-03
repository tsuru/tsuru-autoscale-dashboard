from setuptools import setup, find_packages
import re

verstrline = open("tsuru_autoscale/version.py", "rt").read()
mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string")

setup(
    name="tsuru_autoscale",
    url="https://github.com/tsuru/tsuru-autoscale-dashboard",
    version=version,
    packages=find_packages(),
    description="Web dashboard for tsuru autoscale service",
    author="tsuru",
    author_email="tsuru@corp.globo.com",
    include_package_data=True,
    install_requires=[
        "Django>=1.10.4",
        "requests>=2.8.1",
    ],
)
