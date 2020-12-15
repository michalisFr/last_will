from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='last_will',
    packages=['last_will'],
    version='0.1.9',
    license='MIT',
    description='A program to send encrypted sensitive information to a trusted person in case of your untimely demise',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Michalis Fragkiadakis',
    author_email='michalis.fr@icloud.com',
    url='https://github.com/michalisFr/last_will',
    download_url='https://github.com/michalisFr/last_will/archive/v0.1.9.tar.gz',
    keywords=['encrypted', 'sensitive information', 'failsafe'],
    install_requires=[
        'certifi',
        'chardet',
        'idna',
        'pretty-bad-protocol',
        'psutil',
        'PyJWT',
        'python-crontab',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
        'twilio',
        'urllib3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
