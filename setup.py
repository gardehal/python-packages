import setuptools

# Get requirements requirements.txt, from https://stackoverflow.com/questions/6947988/when-to-use-pip-requirements-file-versus-install-requires-in-setup-py
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setuptools.setup(name="grdUtil",
version="1.5.0",
description="Various Python utility methods, printing, input handling, colouring text in Bash, and more.",
url="https://github.com/grdall/python-packages",
author="grdAll",
install_requires=REQUIREMENTS,
author_email="",
packages=["grdUtil", "grdException", "grdService"],
license="MIT",
zip_safe=False)