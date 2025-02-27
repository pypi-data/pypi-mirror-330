from setuptools import setup, find_packages

# Đọc các phụ thuộc từ requirements.txt
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='tsearch',  # Tên package trên PyPi
    version='1.0.5',
    author='Xakuyay',
    author_email='email@example.com',
    description='Mô tả ngắn gọn về package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/mydb',  # Link tới repo (nếu có)
    packages=find_packages(),  # Tự động tìm tất cả các package con
    install_requires=required_packages,  # Sử dụng các thư viện từ requirements.txt
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
