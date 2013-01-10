# coding: utf-8

# We use setuptools/Distribute because distutils does not seem to support
# the following arguments to setUp().  Passing these arguments to
# setUp() causes a UserWarning to be displayed.
#
#  * entry_points
#  * install_requires
#
import setuptools as dist
setup = dist.setup

PACKAGES = [
    'pizza',
    'pizza.scripts',
    'pizza.scripts.pizza',
    'pizza.scripts.pizza.general',
    # The following packages are only for testing.
    'pizza.test',
    'pizza.test.harness',
    'pizza.test.pizza',
]

setup(name='Pizza',
#      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
#      package_data=package_data,
      entry_points = {
        'console_scripts': [
            'pizza=pizza.scripts.pizza.main:main',
        ],
      },
)
