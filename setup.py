import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pipedrive',
    version='0.1.14',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A Django app to syncronice data with Pipedrive.',
    long_description=README,
    url='https://github.com/MasAval/django_pipedrive',
    autho=r'Gustavo Soto Ridd',
    author_email='gussoto@ug.uchile.cl',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
