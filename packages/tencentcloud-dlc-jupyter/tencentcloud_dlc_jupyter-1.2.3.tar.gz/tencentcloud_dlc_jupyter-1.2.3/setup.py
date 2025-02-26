from setuptools import setup, find_packages
import re
import os
import io

NAME = "tencentcloud-dlc-jupyter"
DESCRIPTION = "Tencentcloud DLC jupyter pulgin. Coding with elastic spark engines in jupyter."
LICENCES = "Apache License Version 2.0"
AUTHOR = "Tencentcloud DLC Team."
MAINTAINER_EMAIL = "valuxzhao@tencent.com"
URL = "https://cloud.tencent.com/product/dlc"
DOWNLOAD_URL = "https://cloud.tencent.com/product/dlc"
PLATFORMS='any'



def read(path, encoding="utf-8"):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()

def version(path):
    
    version_file = read(path)
    version_match = re.search(
        r"""^VERSION = ['"]([^'"]*)['"]""", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = version("tdlc/__init__.py")


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    maintainer_email=MAINTAINER_EMAIL,
    packages=find_packages(exclude=["test*"]),
    platforms=PLATFORMS,
    license=LICENCES,
    # include_package_data=True,
    # package_data={
    # 	'tdlc': {

    # 	}

    # },
    install_requires=[
        "ipython>=7.8.0",
        "numpy",
        "tornado>=4",
        "notebook>=4.2",
        "ipykernel>=4.2.2",
        "nose",
        "pandas",
        "requests",
        "ipywidgets",
        "matplotlib",
        "pyjwt",
    ]
)