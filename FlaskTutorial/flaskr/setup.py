# Used to install the flaskr package
# Specify any files that should be included in the package in MANIFEST.in

from setuptools import setup

setup(
    name='flaskr',
    packages=['flaskr'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)