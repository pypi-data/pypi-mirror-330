#
# Copyright (c)
#    Gammadata GmbH
#    All rights reserved.
#
# Any use of this file as part of a software system by non Copyright holders
# is subject to license terms.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # Here is the module name.
    name="mikrowerk_edi_invoicing",

    # version of the module
    version="0.1.0",

    # Name of Author
    author="Mikrowerk a Gammadata Division",

    # your Email address
    author_email="info@mikrowerk.com",

    # #Small Description about module
    description="Parser for EDI invoices in CII or UBL format",

    # Specifying that we are using markdown file for description
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Any link to reach this module, ***if*** you have any webpage or github profile
    # url="https://github.com/username/",
    packages=setuptools.find_packages(),

    package_dir={"": "."},
    include_package_data=True,
    package_data={'': ['*.yaml', '*.jinja2', '*.sh']},

    # if module has dependencies i.e. if your package rely on other package at pypi.org
    # then you must add there, in order to download every requirement of package

    install_requires=[
        "lxml",
        "pypdf",
        "pytest",
        "flake8",
        "isort",
        "black",
        "coverage",
        "codecov",
        "drafthorse~=2.4.0",
        "factur-x==3.6",
        "jsonpickle~=4.0.1",
        "parameterized",
        "schwifty",
    ],

    license="Affero-3",

    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
