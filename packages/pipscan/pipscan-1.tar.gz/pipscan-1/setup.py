from setuptools import setup, find_packages

setup(
    name="pipscan",  # Name of your package (this is what users will install)
    version="1",  # Version of your package
    packages=find_packages(),  # Automatically finds your package's modules
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="YB",  # Author's name
    description="A Python Library used for network port scanning. Choose between single scanning and multi scanning.",  # Short description
    long_description=open('README.md').read(),  # Detailed description from README
    long_description_content_type="text/markdown",  # Type of long description
    url="https://github.com/yourusername/pipscan",  # URL of your GitHub repo or website
    license="MIT",  # License
)
