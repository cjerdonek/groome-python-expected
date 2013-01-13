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

# Distribute/setuptools does not expose all distutils classes.
from distutils.cmd import Command
import os
import sys

import pizza_setup.utils as utils

PACKAGE_NAME = 'pizza'
# TODO: explore whether I can support distutils (at least for end-users).
USE_DISTRIBUTE = True

dist_version = None

if USE_DISTRIBUTE:
    # Distribute does not seem to support the -r/--repository option
    # with the register command (at least without a [server-login] section
    # in the .pypirc).  See Distribute issue #346 :
    # https://bitbucket.org/tarek/distribute/issue/346/upload-fails-without-server-login-but
    import setuptools
    from setuptools.command.register import register as _register
    from setuptools.command.upload import upload as _upload
    setup = setuptools.setup
    dist = setuptools
    import pkg_resources  # included with Distribute.
    # This is different from setuptools.__version__, which is always '0.6'.
    dist_version = pkg_resources.get_distribution("distribute").version
else:
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

class prep(Command):
    """
    Prepare a release for pushing to PyPI.

    In particular, this updates the long_description file, which should
    be committed prior to pushing to PyPI.

    """
    # Required by distutils.
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        print("testing...")

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
    """
    Call setup() with the correct arguments.

    """
    package_dir = os.path.join(os.path.dirname(__file__), PACKAGE_NAME)
    version = utils.scrape_version(package_dir)

    # TODO: switch to the logging module instead of print().
    print("using: version %s (%s) of %s" %
          (repr(dist.__version__), dist_version, repr(dist)))
    setup(name='Pizza',
          cmdclass = {'prep': prep,
                      'register': register,
                      'upload': upload},
    #      install_requires=INSTALL_REQUIRES,
          packages=PACKAGES,
          long_description='testing 1, 2, 3, 4, 5, 6, 7, 8, testing',
    #      package_data=package_data,
          entry_points = {
            'console_scripts': [
                'pizza=pizza.scripts.pizza.main:main',
            ],
          },
          classifiers=CLASSIFIERS,
          version=version,
    )

if __name__=='__main__':
    main(sys.argv)
