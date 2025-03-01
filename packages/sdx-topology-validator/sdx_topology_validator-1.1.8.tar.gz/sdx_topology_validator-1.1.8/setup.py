from setuptools import setup, find_packages

setup(
    name="sdx_topology_validator",
    version="1.1.8",
    author="Sai Krishna Voruganti",
    author_email="saikrishnavoruganti@gmail.com",
    description="Validates the converted topology against the given OpenAPI specifications",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'sdx_topology_validator': ['validator.yaml']},
    include_package_data=True,
    install_requires=["pyyaml", "jsonref", "jsonschema"],
)
