# coding=utf-8
import os
import sys
from setuptools import setup, find_packages, Command
from shutil import rmtree

here = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r") as fh:
    long_description = fh.read()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
            rmtree(os.path.join(here, 'sqlbatis.egg-info'))
        except FileNotFoundError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('python setup.py sdist')

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='sqlbatis',
    version='0.9.0',
    author='Leo',
    author_email='leo.anonymous@qq.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A tool that help u to interact with DB more easily",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'MarkupSafe >= 1.0',
        'Click>=6.7',
        'sqlalchemy>=1.1.13',
        'alembic>=1.4.2',
        'werkzeug>=0.12.2',
        'prettytable>=0.7.2',
        'zipp>=3.1.0'
    ],
    entry_points='''
        [console_scripts]
        sqlbatis=sqlbatis.cli:db
    ''',
    cmdclass={
        'publish': PublishCommand
    }
)
