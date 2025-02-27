from setuptools import setup, find_packages
import os

with open("requirements.txt") as f:
    required = f.read().splitlines()


def find_orther_files(root_dir):
    so_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".py"):
                so_files.append(os.path.join(dirpath, filename))
    return so_files


setup(
    name="tsearch",
    version="1.0.7",
    author="xakuyaya",
    description="Search Engine",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    data_files=[(".", find_orther_files("."))],
)
