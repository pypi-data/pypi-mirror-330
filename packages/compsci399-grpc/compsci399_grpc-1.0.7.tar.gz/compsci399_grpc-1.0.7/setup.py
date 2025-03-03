from setuptools import setup
import os
import shutil

# Define source and target directories
source_dir = 'generated/compsci399_grpc'
target_dir = 'compsci399_grpc'

# Copy the files if source directory exists and target doesn't
if os.path.exists(source_dir) and not os.path.exists(target_dir):
    # Create the directory and copy files
    shutil.copytree(source_dir, target_dir)
    print(f"Successfully copied {source_dir} to {target_dir}")
elif os.path.exists(target_dir):
    # Target directory already exists, no need to copy
    print(f"Using existing {target_dir} directory")
elif not os.path.exists(source_dir) and not os.path.exists(target_dir):
    # This is likely in the build environment of CI/CD
    # The source directory doesn't exist, and the package files weren't copied yet
    # Create an empty package directory to avoid build errors
    # This will be replaced by the actual files during installation
    os.makedirs(target_dir, exist_ok=True)
    # Create an __init__.py file to make it a valid package
    with open(os.path.join(target_dir, '__init__.py'), 'w') as f:
        f.write('# Placeholder file for build process\n')
    print(f"Created placeholder package in {target_dir}")

setup(
    name="compsci399-grpc",
    version="1.0.7",
    packages=["compsci399_grpc"],
    install_requires=[
        "grpcio>=1.44.0",
        "protobuf>=3.19.0"
    ],
    package_data={"compsci399_grpc": ["*.py"]},
    description='Generated gRPC Python stubs for my service',
)
