from setuptools import setup, find_namespace_packages

setup(
    name="compsci399-grpc",
    version="1.0.6",
    packages=find_namespace_packages(include=["generated.*"]),
    install_requires=[
        "grpcio>=1.44.0",
        "protobuf>=3.19.0"
    ],
    package_data={"": ["*.py"]},
)
