import os
from setuptools import (
    find_packages,
    setup,
)

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'slice_aggregator', '__about__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name='slice-aggregator',
    version=about['__version__'],
    packages=find_packages(exclude=['tests']),
    python_requires=">=3.5",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'numpy'],
)
