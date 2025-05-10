# pip install -e .
# TODO: switch to pyproject.toml

from setuptools import setup, find_packages
# from distutils.core import setup

setup(
    name='threaded_fastener_tools',
    version='0.0.1',  # major.minor[.patch[.sub]]
    description='tools for analyzing threaded fasteners',
    url=None,
    author='Timothy P Woodard',
    author_email='timothy.woodard.809@outlook.com',
    license='General Purpose',
    packages=['threaded_fastener_tools'],
    package_dir={'': 'src'},
    install_requires=[
        'json',
        'numpy', 
        'scipy',
        'matplotlib',
    ]
)
