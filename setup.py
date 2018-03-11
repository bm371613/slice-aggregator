from setuptools import (
    find_packages,
    setup,
)

setup(
    name='slice-aggregator',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    python_requires=">=3.5",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
