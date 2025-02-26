from setuptools import setup, find_packages

setup(
    name="vtb-logger",
    version="2.4.0",
    author="VTB Wanderer DG",
    author_email="vtb.wanderers63@gmail.com",
    description="A simple Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vtb-wanderers63/py-logging-module",
    packages=find_packages(),
    install_requires=[
        "confluent-kafka",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
