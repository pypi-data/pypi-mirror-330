from setuptools import setup,find_packages


with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name='smart_pyxl',
    version='0.0.1-beta',
    description='Handle merged cells in excel files',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        "pandas >= 2.2.3",
        "openpyxl >= 3.1.0",
    ],
    zip_safe=False)