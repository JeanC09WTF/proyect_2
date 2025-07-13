from setuptools import setup, find_packages

setup(
    name="proyect_2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0.0',
        'pytest>=7.0.0',
        'pytest-xdist>=3.0.0'
    ],
    python_requires='>=3.10',
)
