# coding: utf-8

"""


"""


# We use setuptools/Distribute because distutils does not seem to support
# the following arguments to setUp().  Passing these arguments to
# setUp() causes a UserWarning to be displayed.
#
#  * entry_points
#  * install_requires
#

import sys

# TODO: explore whether I can support distutils (at least for end-users).
USE_SETUPTOOLS = False

if USE_SETUPTOOLS:
    import setuptools
    from setuptools.command.register import register as _register
    from setuptools.command.upload import upload as _upload
    setup = setuptools.setup
    dist = setuptools
else:
    import distutils
    from distutils.command.register import register as _register
    from distutils.command.upload import upload as _upload
    from distutils.core import setup
    dist = distutils


# TODO: configure logging simply.


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

def prompt(command):
    command_name = command.get_command_name()
    # The repository attribute is the URL.
    answer = raw_input("Are you sure you want to %s to %s (yes/no)? " %
                       (command_name, command.repository))
    if answer != "yes":
        sys.exit("aborted: %s" % command_name)

# Subclass so we can prompt before writing to PyPI.
class upload(_upload):
    def run(self):
        prompt(self)
        return _upload.run(self)

# Subclass so we can prompt before writing to PyPI.
class register(_register):
    # We override post_to_server() instead of run() because finalize_options()
    # and self._set_config() are called at the beginning of run().
    def post_to_server(self, data, auth=None):
        prompt(self)
        return _register.post_to_server(self, data, auth=auth)

CLASSIFIERS = (
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: PyPy',
)

def main(sys_argv):
    # TODO: switch to the logging module instead of print().
    print("using: version %s of %s" % (repr(dist.__version__), repr(dist)))
    setup(name='Pizza',
          cmdclass = {'register': register, 'upload': upload},
    #      install_requires=INSTALL_REQUIRES,
          packages=PACKAGES,
          long_description='testing 1, 2, 3, 4, 5, testing',
    #      package_data=package_data,
          entry_points = {
            'console_scripts': [
                'pizza=pizza.scripts.pizza.main:main',
            ],
          },
          classifiers=CLASSIFIERS,
    )

if __name__=='__main__':
    main(sys.argv)
