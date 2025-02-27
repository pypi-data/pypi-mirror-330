from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hyyap',
    version='0.0.1',
    description='hyyap',
    long_description=long_description,
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=find_packages(),
    package_data={
        "hyyap": ['*.exe'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        "tqdm",
        "rich",
        "requests",
        "py7zr",
        "pipreqs",
        "python-pptx",
        "openpyxl",
        "python-docx",
        "beautifulsoup4",
        "pillow",
        "pynvml",
        "wmi",
        "pywin32",
        "psutil",
    ],
)