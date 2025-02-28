import os
import io
import setuptools


name = "tmg-data"
description = "TMG data library"
version = "0.2.14"
dependencies = [
    "oauth2client==4.1.3",
    "google-api-python-client==2.100.0",
    "google-cloud-bigquery==3.19.0",
    "google-cloud-storage==2.15.0",
    "paramiko==2.8.0",
    "Jinja2==2.11.2",
    "mysql-connector==2.2.9",
    "boto3==1.14.8",
    "simple-salesforce==1.10.1",
    "parse==1.15.0",
    "delegator.py==0.1.1",
    "markupsafe==2.0.1",
    "pandas==2.0.1"
]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author='TMG Data Platform team',
    author_email="data.platform@telegraph.co.uk",
    license="Apache 2.0",
    url='https://github.com/telegraph/tmg-data',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    python_requires='>=3.6',

)
