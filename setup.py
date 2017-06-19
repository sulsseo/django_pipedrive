import os
import pypandoc
from setuptools import find_packages, setup, Command

try:
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")
except OSError as e:
    print("\n\n!!! pandoc not found, long_description is bad, don't upload this to PyPI !!!\n\n")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()


class DownloadPandocCommand(Command):

    """Download pandoc"""

    description = "downloads a pandoc release and adds it to the package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from pypandoc.pandoc_download import download_pandoc
        targetfolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pypandoc", "files")
        download_pandoc(targetfolder=targetfolder)


cmd_classes = {'download_pandoc': DownloadPandocCommand}


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pipedrive',
    version='0.1.14',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A Django app to syncronice data with Pipedrive.',
    long_description=long_description,
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
    cmdclass=cmd_classes,
)
