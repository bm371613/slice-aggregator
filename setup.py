import os
from setuptools import (
    find_packages,
    setup,
)

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'slice_aggregator', '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(here, 'requirements', 'tests.txt')) as f:
    tests_require = list(f.read().split('\n'))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='slice-aggregator',
    version=about['__version__'],
    description=
    'A library for aggregating values assigned to indices by slices and the other way around ',
    long_description=README,
    url='https://github.com/bm371613/slice-aggregator',
    author='Bartosz Marcinkowski',
    author_email='bm371613@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
        'Documentation': 'https://slice-aggregator.readthedocs.io/',
        'Source': 'https://github.com/bm371613/slice-aggregator/',
        'Tracker': 'https://github.com/bm371613/slice-aggregator/issues',
    },
    packages=find_packages(exclude=['tests']),
    python_requires=">=3.5",
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
)
