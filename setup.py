import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-htmx-renderer',
    version='0.0.1',
    packages=['htmx_renderer', ],
    include_package_data=True,
    license='MIT License',
    description='HTMX renderer for Django REST FRAMEWORK',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/nanuxbe/drf_htmx_renderer',
    author='Emmanuelle Delescolle',
    author_email='info@levit.be',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=3.2',
        'drf-schema-adapter>=3.0.0',
    ]
)

