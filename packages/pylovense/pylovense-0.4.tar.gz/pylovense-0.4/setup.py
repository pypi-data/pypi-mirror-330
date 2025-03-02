from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pylovense',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='jinxed-catgirl',
    description='A python wrapper for the Lovense API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    keywords='lovense api wrapper',
)