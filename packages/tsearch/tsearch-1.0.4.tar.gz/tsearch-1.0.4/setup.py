from setuptools import setup, find_packages
import os

def find_other_files(root_dir, extensions=(".so", ".yaml", ".json", ".md")):
    other_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extensions):
                # Lấy đường dẫn tương đối để đóng gói đúng
                relative_path = os.path.relpath(os.path.join(dirpath, filename), start=".")
                other_files.append(relative_path)
    return other_files

setup(
    name="tsearch",
    version="1.0.4",
    author="xakuyaya",
    description="Search Engine",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=open("requirements.txt", "r", encoding="utf-8").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        "": find_other_files("."),
    },
    python_requires=">=3.6",
)
