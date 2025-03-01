import os
import re
import setuptools

# Read version from version.py
with open(os.path.join("src", "airflow", "providers", "filemaker", "version.py"), "r") as version_file:
    version_content = version_file.read()
    VERSION = re.search(r'__version__ = ["\']([^"\']+)["\']', version_content).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arktci-airflow-provider-filemaker",
    version=VERSION,
    author="Josh Lipton @ ArkTCI",
    author_email="josh@arktci.com",
    description="Apache Airflow provider for FileMaker Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArkTCI/airflow-providers",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(include=["airflow.providers.*"], where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'apache-airflow>=2.0.0',
        'boto3>=1.16.0',
        'requests>=2.25.0',
        'pandas>=1.0.0'
    ],
    entry_points={
        "apache_airflow_provider": [
            "provider_info=airflow.providers.filemaker:get_provider_info"
        ]
    }
) 