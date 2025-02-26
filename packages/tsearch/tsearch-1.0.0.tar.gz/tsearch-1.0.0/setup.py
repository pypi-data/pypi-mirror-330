from setuptools import setup, find_packages
import os

FOLDER = "mydb_converted"
# Đọc yêu cầu từ requirements.txt (sử dụng đường dẫn tương đối)
with open(f"{FOLDER}/requirements.txt", "r", encoding="utf-8") as f:
    required = f.read().splitlines()


# Tìm các file không phải .py trong thư mục (trả về đường dẫn tương đối)
def find_other_files(root_dir):
    so_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".py"):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), start=root_dir)
                so_files.append(relative_path)
    return so_files


setup(
    name="tsearch",
    version="1.0.0",
    author="xakuyaya",
    description="Search Engine",
    long_description=open(f"{FOLDER}/README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="binsearch_converted"),
    package_dir={"": f"{FOLDER}"},
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        "": find_other_files(f"{FOLDER}"),  # Sử dụng đường dẫn tương đối
    },
    python_requires='>=3.6',
)
